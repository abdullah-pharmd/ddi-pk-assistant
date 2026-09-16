"""
Clinical Pharmacokinetics & Drug Interaction Decision Support Assistant
Faculty of Pharmaceutical Sciences | Clinical Decision Support Prototype
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
from renal import crcl_cockcroft_gault, renal_category
from pk_engine import gentamicin_pk, vancomycin_pk, digoxin_pk, phenytoin_pk, winter_tozer_correction
from ddi_engine import DDIEngine
from tdm import interpret_tdm
from dose_adjustment import assess_dose_adjustment
from batch_processing import validate_csv_rows, group_by_patient, parse_csv_text, results_to_csv
from report_generator import generate_report
import tempfile

st.set_page_config(
    page_title="Clinical PK & DDI Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom High-End Clinical Light Theme CSS
st.markdown("""
<style>
    /* Force pristine light background and crisp typography */
    .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    
    /* Hide default Streamlit clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Academic / Hospital Header Banner - Pure Clinical Light */
    .hospital-header {
        background: #FFFFFF;
        border-top: 4px solid #1E40AF;
        border-bottom: 1px solid #E2E8F0;
        border-left: 1px solid #E2E8F0;
        border-right: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    }
    .hospital-subtitle {
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #1E40AF;
        margin-bottom: 0.35rem;
    }
    .hospital-title {
        font-size: 1.65rem;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.02em;
        margin: 0 0 0.4rem 0;
        line-height: 1.25;
    }
    .hospital-desc {
        font-size: 0.88rem;
        color: #475569;
        margin: 0;
        line-height: 1.5;
    }
    
    /* Clinical Card Component */
    .card-surface {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    }
    
    /* Metric Cards - High-Precision Lab Readout */
    .lab-metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
        gap: 0.75rem;
        margin: 0.75rem 0;
    }
    .lab-metric-box {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 0.75rem 0.9rem;
    }
    .lab-metric-label {
        font-size: 0.72rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 0.25rem;
    }
    .lab-metric-val {
        font-size: 1.35rem;
        font-weight: 700;
        color: #0F172A;
        font-variant-numeric: tabular-nums;
        line-height: 1.2;
    }
    .lab-metric-unit {
        font-size: 0.75rem;
        font-weight: 500;
        color: #64748B;
        margin-left: 0.2rem;
    }
    
    /* Primary Target Card Highlight */
    .lab-metric-target {
        background: #EFF6FF;
        border: 1px solid #BFDBFE;
    }
    .lab-metric-target .lab-metric-label {
        color: #1D4ED8;
    }
    .lab-metric-target .lab-metric-val {
        color: #1E40AF;
    }

    /* Clinical Triage Badges */
    .triage-card {
        background: #FFFFFF;
        border-radius: 6px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    }
    .triage-high {
        border-left: 4px solid #DC2626;
        border-top: 1px solid #FEE2E2;
        border-right: 1px solid #FEE2E2;
        border-bottom: 1px solid #FEE2E2;
        background: #FFFDFD;
    }
    .triage-mod {
        border-left: 4px solid #D97706;
        border-top: 1px solid #FEF3C7;
        border-right: 1px solid #FEF3C7;
        border-bottom: 1px solid #FEF3C7;
        background: #FFFEF9;
    }
    .triage-artifact {
        border-left: 4px solid #7C3AED;
        border-top: 1px solid #EDE9FE;
        border-right: 1px solid #EDE9FE;
        border-bottom: 1px solid #EDE9FE;
        background: #FCFAFF;
    }
    .triage-none {
        border-left: 4px solid #16A34A;
        border: 1px solid #E2E8F0;
        border-left-width: 4px;
        background: #FAFCFA;
    }

    /* Staging Pills */
    .stage-badge {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 4px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    .stage-normal { background: #DCFCE7; color: #166534; border: 1px solid #BBF7D0; }
    .stage-mild { background: #FEF9C3; color: #854D0E; border: 1px solid #FEF08A; }
    .stage-moderate { background: #FFEDD5; color: #9A3412; border: 1px solid #FED7AA; }
    .stage-severe { background: #FEE2E2; color: #991B1B; border: 1px solid #FECACA; }
    .stage-esrd { background: #450A0A; color: #FEF2F2; }

    /* Clean Streamlit Tab Bars */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-bottom: 1px solid #CBD5E1 !important;
        gap: 1.5rem !important;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 0.6rem 0.2rem !important;
        color: #64748B !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        border: none !important;
        background: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: #1E40AF !important;
        border-bottom: 2px solid #1E40AF !important;
    }

    /* Buttons */
    .stButton>button {
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.88rem;
        padding: 0.55rem 1.25rem;
        letter-spacing: 0.01em;
    }
</style>
""", unsafe_allow_html=True)

# Hospital / Academic Brand Header
st.markdown("""
<div class="hospital-header">
    <div class="hospital-subtitle">Faculty of Pharmaceutical Sciences • Clinical Decision Support Systems Research</div>
    <div class="hospital-title">Clinical Pharmacokinetics & Drug Interaction Assistant</div>
    <div class="hospital-desc">Deterministic renal clearance staging (Cockcroft-Gault), classical single- and non-linear pharmacokinetic modeling (Bauer 2nd ed.), and alert-fatigue-filtered drug-drug interaction surveillance.</div>
</div>
""", unsafe_allow_html=True)

DRUGS = ["Gentamicin", "Vancomycin", "Digoxin", "Phenytoin"]
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "ddi_knowledge_base.csv")

tab_single, tab_batch = st.tabs(["Single Patient Clinical Workstation", "Batch Cohort Analysis (CSV)"])

# ============================================================
# TAB 1: Single Patient Clinical Workstation
# ============================================================
with tab_single:
    col_input, col_renal = st.columns([3, 2])
    
    with col_input:
        st.markdown("##### 1. Patient Demographics & Intake")
        c1, c2, c3 = st.columns(3)
        with c1:
            age = st.number_input("Age (years)", min_value=1, max_value=120, value=65)
            sex = st.selectbox("Biological Sex", ["male", "female"])
        with c2:
            weight_kg = st.number_input("Total Weight (kg)", min_value=1.0, value=70.0, step=0.5)
            height_cm = st.number_input("Height (cm)", min_value=50.0, value=175.0, step=0.5)
        with c3:
            scr = st.number_input("Serum Creatinine (mg/dL)", min_value=0.1, value=1.0, step=0.1)
            hepatic_flag = st.checkbox("Hepatic Impairment Documented", value=False)
        
        st.markdown("##### Target Pharmacotherapy")
        selected_drugs = st.multiselect(
            "Select medications for concurrent regimen evaluation",
            DRUGS,
            default=["Vancomycin", "Gentamicin"]
        )
        
        nyha_class = "I"
        if "Digoxin" in selected_drugs:
            nyha_class = st.selectbox(
                "NYHA Heart Failure Class (determines non-renal clearance)",
                ["I", "II", "III", "IV"],
                index=0
            )

    # Renal Function Evaluation
    try:
        renal_result = crcl_cockcroft_gault(age, weight_kg, height_cm, sex, scr)
        cat_result = renal_category(renal_result["crcl_ml_min"])
        crcl_val = renal_result["crcl_ml_min"]
        category = cat_result["category"]
        
        stage_class = {
            "Normal": "stage-normal",
            "Mild": "stage-mild",
            "Moderate": "stage-moderate",
            "Severe": "stage-severe",
            "ESRD": "stage-esrd"
        }.get(category, "stage-mild")
        
        with col_renal:
            st.markdown("##### 2. Renal Clearance Staging")
            st.markdown(f"""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:1.2rem; box-shadow:0 1px 2px rgba(0,0,0,0.02);">
                <div style="font-size:0.75rem; color:#64748B; font-weight:700; text-transform:uppercase; letter-spacing:0.04em;">Estimated Creatinine Clearance</div>
                <div style="font-size:2.2rem; font-weight:800; color:#0F172A; margin:0.25rem 0; font-variant-numeric:tabular-nums;">
                    {crcl_val:.1f} <span style="font-size:1rem; font-weight:500; color:#64748B;">mL/min</span>
                </div>
                <div style="margin: 0.4rem 0 0.8rem 0;">
                    <span class="stage-badge {stage_class}">{category} Renal Impairment</span>
                </div>
                <div style="font-size:0.8rem; color:#475569; border-top:1px solid #F1F5F9; padding-top:0.6rem; line-height:1.5;">
                    <b>Dosing Weight Basis:</b> {renal_result['weight_basis'].capitalize()}<br/>
                    <b>Method:</b> Cockcroft-Gault (1976) | FDA Guidance Staging
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    except ValueError as e:
        st.error(f"Renal computation error: {e}")
        st.stop()

    st.markdown("---")

    # Pharmacokinetic Modeling Panels
    st.markdown("##### 3. Individualized Pharmacokinetic Profile")
    if not selected_drugs:
        st.info("Select one or more medications above to compute individualized pharmacokinetic parameters.")
    
    pk_results = {}
    for drug in selected_drugs:
        try:
            if drug == "Gentamicin":
                res = gentamicin_pk(weight_kg, renal_result["crcl_ml_min"], height_cm, sex)
                pk_results[drug] = res
                st.markdown(f"""
                <div class="card-surface">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;">
                        <span style="font-size:1.05rem; font-weight:700; color:#0F172A;">Gentamicin (IV One-Compartment Model)</span>
                        <span style="font-size:0.75rem; background:#F1F5F9; color:#475569; padding:0.2rem 0.5rem; border-radius:4px; font-weight:600;">Aminoglycoside</span>
                    </div>
                    <div class="lab-metric-grid">
                        <div class="lab-metric-box">
                            <div class="lab-metric-label">Distribution Vol (Vd)</div>
                            <div class="lab-metric-val">{res['vd_l']}<span class="lab-metric-unit">L</span></div>
                        </div>
                        <div class="lab-metric-box">
                            <div class="lab-metric-label">Elimination Rate (ke)</div>
                            <div class="lab-metric-val">{res['ke_per_hr']:.4f}<span class="lab-metric-unit">hr⁻¹</span></div>
                        </div>
                        <div class="lab-metric-box">
                            <div class="lab-metric-label">Systemic Clearance</div>
                            <div class="lab-metric-val">{res['cl_l_hr']:.2f}<span class="lab-metric-unit">L/hr</span></div>
                        </div>
                        <div class="lab-metric-box">
                            <div class="lab-metric-label">Half-Life (t½)</div>
                            <div class="lab-metric-val">{res['half_life_hr']:.1f}<span class="lab-metric-unit">hr</span></div>
                        </div>
                        <div class="lab-metric-box lab-metric-target">
                            <div class="lab-metric-label">Initial Loading Dose</div>
                            <div class="lab-metric-val">{res['loading_dose_mg']:.0f}<span class="lab-metric-unit">mg</span></div>
                        </div>
                    </div>
                    <div style="font-size:0.75rem; color:#64748B; margin-top:0.5rem;">
                        <b>Equation Trace:</b> ke = 0.00293 × CrCl + 0.014 | Vd = 0.26 L/kg | Bauer Applied Clinical Pharmacokinetics (2nd ed., Ch.4)
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            elif drug == "Vancomycin":
                res = vancomycin_pk(weight_kg, renal_result["crcl_ml_min"], height_cm, sex)
                pk_results[drug] = res
                st.markdown(f"""
                <div class="card-surface">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;">
                        <span style="font-size:1.05rem; font-weight:700; color:#0F172A;">Vancomycin (Matzke Weight-Adjusted Model)</span>
                        <span style="font-size:0.75rem; background:#F1F5F9; color:#475569; padding:0.2rem 0.5rem; border-radius:4px; font-weight:600;">Glycopeptide</span>
                    </div>
                    <div class="lab-metric-grid">
                        <div class="lab-metric-box">
                            <div class="lab-metric-label">Distribution Vol (Vd)</div>
                            <div class="lab-metric-val">{res['vd_l']}<span class="lab-metric-unit">L</span></div>
                        </div>
                        <div class="lab-metric-box">
                            <div class="lab-metric-label">Systemic CL</div>
                            <div class="lab-metric-val">{res['cl_ml_min']:.1f}<span class="lab-metric-unit">mL/min</span></div>
                        </div>
                        <div class="lab-metric-box">
                            <div class="lab-metric-label">Elimination (k)</div>
                            <div class="lab-metric-val">{res['k_per_hr']:.4f}<span class="lab-metric-unit">hr⁻¹</span></div>
                        </div>
                        <div class="lab-metric-box">
                            <div class="lab-metric-label">Half-Life (t½)</div>
                            <div class="lab-metric-val">{res['half_life_hr']:.1f}<span class="lab-metric-unit">hr</span></div>
                        </div>
                        <div class="lab-metric-box lab-metric-target">
                            <div class="lab-metric-label">Target Daily Dose (AUC 500)</div>
                            <div class="lab-metric-val">{res['daily_dose_mg']:.0f}<span class="lab-metric-unit">mg/day</span></div>
                        </div>
                    </div>
                    <div style="font-size:0.75rem; color:#64748B; margin-top:0.5rem;">
                        <b>Equation Trace:</b> CL = 0.695 × CrCl + 0.05 × Wt | Target AUC24 500 mg·hr/L (ASHP-IDSA) | Bauer Ch.5
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            elif drug == "Digoxin":
                res = digoxin_pk(weight_kg, renal_result["crcl_ml_min"], nyha_class, height_cm, sex)
                pk_results[drug] = res
                st.markdown(f"""
                <div class="card-surface">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;">
                        <span style="font-size:1.05rem; font-weight:700; color:#0F172A;">Digoxin (Jusko-Koup Two-Compartment Model)</span>
                        <span style="font-size:0.75rem; background:#F1F5F9; color:#475569; padding:0.2rem 0.5rem; border-radius:4px; font-weight:600;">Cardiac Glycoside (NYHA {nyha_class})</span>
                    </div>
                    <div class="lab-metric-grid">
                        <div class="lab-metric-box">
                            <div class="lab-metric-label">Distribution Vol (Vd)</div>
                            <div class="lab-metric-val">{res['vd_l']:.0f}<span class="lab-metric-unit">L</span></div>
                        </div>
                        <div class="lab-metric-box">
                            <div class="lab-metric-label">Total Clearance</div>
                            <div class="lab-metric-val">{res['cl_ml_min']:.1f}<span class="lab-metric-unit">mL/min</span></div>
                        </div>
                        <div class="lab-metric-box">
                            <div class="lab-metric-label">Non-Renal CL (Heart Failure)</div>
                            <div class="lab-metric-val">{res['cl_nr_used']}<span class="lab-metric-unit">mL/min</span></div>
                        </div>
                        <div class="lab-metric-box">
                            <div class="lab-metric-label">Half-Life (t½)</div>
                            <div class="lab-metric-val">{res['half_life_hr']:.1f}<span class="lab-metric-unit">hr</span></div>
                        </div>
                    </div>
                    <div style="font-size:0.75rem; color:#64748B; margin-top:0.5rem;">
                        <b>Equation Trace:</b> CL = 1.303 × CrCl + ClNR(NYHA) | Bauer Ch.6 pp.305-314
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            elif drug == "Phenytoin":
                css_target = st.number_input("Target Steady-State Css (mg/L)", min_value=5.0, max_value=25.0, value=15.0, step=1.0)
                res = phenytoin_pk(weight_kg, css_target, height_cm, sex)
                pk_results[drug] = res
                st.markdown(f"""
                <div class="card-surface">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;">
                        <span style="font-size:1.05rem; font-weight:700; color:#0F172A;">Phenytoin (Michaelis-Menten Capacity-Limited Kinetics)</span>
                        <span style="font-size:0.75rem; background:#F1F5F9; color:#475569; padding:0.2rem 0.5rem; border-radius:4px; font-weight:600;">Antiepileptic</span>
                    </div>
                    <div class="lab-metric-grid">
                        <div class="lab-metric-box">
                            <div class="lab-metric-label">Max Velocity (Vmax)</div>
                            <div class="lab-metric-val">{res['vmax_mg_day']:.0f}<span class="lab-metric-unit">mg/day</span></div>
                        </div>
                        <div class="lab-metric-box">
                            <div class="lab-metric-label">Michaelis Const (Km)</div>
                            <div class="lab-metric-val">{res['km_mg_l']}<span class="lab-metric-unit">mg/L</span></div>
                        </div>
                        <div class="lab-metric-box">
                            <div class="lab-metric-label">Target Css</div>
                            <div class="lab-metric-val">{res['css_target_mg_l']}<span class="lab-metric-unit">mg/L</span></div>
                        </div>
                        <div class="lab-metric-box lab-metric-target">
                            <div class="lab-metric-label">Calculated Daily Dose</div>
                            <div class="lab-metric-val">{res['dose_mg_day']:.0f}<span class="lab-metric-unit">mg/day</span></div>
                        </div>
                    </div>
                    <div style="font-size:0.75rem; color:#64748B; margin-top:0.5rem;">
                        <b>Equation Trace:</b> Dose = (Vmax × Css) / (Km + Css) | Richens & Dunlop (Lancet 1975); Bauer Ch.10
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
        except (ValueError, NotImplementedError) as e:
            st.error(f"{drug} parameter calculation: {e}")

    st.markdown("---")

    # Drug-Drug Interaction Surveillance
    st.markdown("##### 4. Drug-Drug Interaction Surveillance")
    ddi_findings = []
    if len(selected_drugs) >= 2:
        try:
            engine = DDIEngine(DATA_PATH)
            ddi_findings = engine.check_all_pairs(selected_drugs)
            
            for f in ddi_findings:
                if f["pair_found_in_kb"]:
                    sev = f["severity"]
                    is_artifact = "immuno" in f["effect"].lower() or "petinia" in f["effect"].lower()
                    
                    if is_artifact:
                        card_class = "triage-artifact"
                        badge_label = "ANALYTICAL ASSAY ARTIFACT"
                        badge_style = "background:#EDE9FE; color:#6D28D9; border:1px solid #DDD6FE;"
                    elif sev == "High":
                        card_class = "triage-high"
                        badge_label = "CRITICAL CONTRAINDICATION"
                        badge_style = "background:#FEE2E2; color:#B91C1C; border:1px solid #FECACA;"
                    else:
                        card_class = "triage-mod"
                        badge_label = "CLINICAL MONITORING REQUIRED"
                        badge_style = "background:#FEF3C7; color:#B45309; border:1px solid #FDE68A;"
                    
                    st.markdown(f"""
                    <div class="triage-card {card_class}">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
                            <span style="font-size:1rem; font-weight:700; color:#0F172A;">{f['drug_a']} + {f['drug_b']}</span>
                            <span style="font-size:0.72rem; font-weight:700; padding:0.2rem 0.55rem; border-radius:4px; {badge_style}">{badge_label}</span>
                        </div>
                        <div style="font-size:0.86rem; color:#334155; line-height:1.45; margin:0.25rem 0;"><b>Mechanism:</b> {f['effect']}</div>
                        <div style="font-size:0.86rem; color:#334155; line-height:1.45; margin:0.25rem 0;"><b>Recommendation:</b> {f['clinical_recommendation']}</div>
                        <div style="font-size:0.75rem; color:#64748B; margin-top:0.35rem;"><b>Reference:</b> {f['reference']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="triage-card triage-none">
                        <div style="font-size:0.92rem; font-weight:700; color:#15803D; margin-bottom:0.2rem;">{f['drug_a']} + {f['drug_b']} — No High-Tier Interaction in Knowledge Base</div>
                        <div style="font-size:0.8rem; color:#64748B;">{f['note']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        except FileNotFoundError:
            st.warning("DDI database file not located at expected path.")
    else:
        st.info("Select at least two concurrent medications above to activate pairwise interaction screening.")

    st.markdown("---")

    # Clinical Regimen Synthesis & Adjustment
    st.markdown("##### 5. Integrated Regimen Synthesis & Dose Guidance")
    adjustment = assess_dose_adjustment(
        renal_category=cat_result["category"],
        ddi_findings=ddi_findings,
        tdm_status=None,
        hepatic_flag=hepatic_flag,
    )
    
    if adjustment["adjustment_indicated"]:
        st.markdown("""
        <div style="background:#FFFBEB; border:1px solid #FCD34D; border-radius:6px; padding:1rem 1.25rem; margin-bottom:1rem;">
            <div style="font-size:0.92rem; font-weight:700; color:#92400E; margin-bottom:0.35rem;">⚠️ Clinical Dosage Adjustment Triggered</div>
        """, unsafe_allow_html=True)
        for reason in adjustment["reasons"]:
            st.markdown(f"- **{reason}**")
        st.markdown(f"""
            <div style="font-size:0.75rem; color:#78350F; margin-top:0.4rem; font-style:italic;">{adjustment['note']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:6px; padding:1rem 1.25rem; margin-bottom:1rem;">
            <div style="font-size:0.92rem; font-weight:700; color:#166534;">✓ Standard Regimen Maintained</div>
            <div style="font-size:0.84rem; color:#15803D;">Patient renal clearance is preserved and no high-severity interacting co-medications were identified.</div>
        </div>
        """, unsafe_allow_html=True)

    # PDF Report Export Section
    st.markdown("---")
    st.markdown("##### 6. Clinical Audit Documentation")
    st.caption("Generate an auditable, timestamped clinical PDF summary containing all input variables, equation traces, and interaction advisories.")
    
    if st.button("Generate Audited Clinical PDF Report", type="primary"):
        patient_info = {
            "Age": age, "Sex": sex, "Weight (kg)": weight_kg, "Height (cm)": height_cm,
            "SCr (mg/dL)": scr, "Hepatic Impairment": "Documented" if hepatic_flag else "None",
            "Medications": ", ".join(selected_drugs),
        }
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            generate_report(tmp.name, patient_info, renal_result, cat_result,
                            pk_results, ddi_findings, adjustment)
            with open(tmp.name, "rb") as f:
                st.download_button(
                    "Download Official PDF Summary",
                    f.read(),
                    file_name=f"Clinical_PK_Report_Pt_{age}_{sex[0].upper()}.pdf",
                    mime="application/pdf"
                )

# ============================================================
# TAB 2: Batch (CSV Upload)
# ============================================================
with tab_batch:
    st.markdown("##### Inpatient Ward Cohort Screening")
    st.caption("Screen multiple hospital bed charts simultaneously by uploading a standardized multi-row CSV.")
    
    uploaded_file = st.file_uploader("Upload patient cohort CSV", type=["csv"])

    if uploaded_file is not None:
        csv_text = uploaded_file.getvalue().decode("utf-8")
        rows = parse_csv_text(csv_text)
        errors = validate_csv_rows(rows)

        if errors:
            st.error("Validation failed — please fix the following row issues:")
            for err in errors:
                st.markdown(f"- {err}")
        else:
            st.success(f"Validated {len(rows)} patient rows. Executing clinical screening...")
            patients = group_by_patient(rows)
            engine = DDIEngine(DATA_PATH)
            results = []

            for pid, p in patients.items():
                try:
                    renal = crcl_cockcroft_gault(p["age"], p["weight_kg"], p["height_cm"],
                                                  p["sex"], p["scr_mg_dl"])
                    cat = renal_category(renal["crcl_ml_min"])
                    ddi_findings = engine.check_all_pairs(p["drugs"]) if len(p["drugs"]) >= 2 else []
                    adjustment = assess_dose_adjustment(
                        cat["category"], ddi_findings, hepatic_flag=p["hepatic_impairment"]
                    )
                    results.append({
                        "Patient ID": pid,
                        "CrCl (mL/min)": renal["crcl_ml_min"],
                        "Renal Stage": cat["category"],
                        "Regimen": "; ".join(p["drugs"]),
                        "Adjustment Needed": "YES" if adjustment["adjustment_indicated"] else "NO",
                        "Clinical Flags": " | ".join(adjustment["reasons"]) if adjustment["reasons"] else "None",
                    })
                except (ValueError, NotImplementedError) as e:
                    results.append({
                        "Patient ID": pid, "CrCl (mL/min)": None, "Renal Stage": "Error",
                        "Regimen": "; ".join(p["drugs"]), "Adjustment Needed": "ERROR",
                        "Clinical Flags": str(e),
                    })

            st.dataframe(results, use_container_width=True)
            csv_out = results_to_csv(results)
            st.download_button(
                "Export Processed Ward Cohort (CSV)",
                csv_out,
                file_name="cohort_screening_results.csv",
                mime="text/csv"
            )

# Footer
st.markdown("---")
st.caption(
    "Clinical Pharmacokinetics & Drug-Drug Interaction Assistant • Faculty of Pharmaceutical Sciences, "
    "Government College University Faisalabad • Deterministic Clinical Models from Larry A. Bauer Applied Clinical Pharmacokinetics (2nd ed.)"
)
