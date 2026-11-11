/* ===== CASS Intelligence Reports -- Portal App ===== */
'use strict';

// -- SVG icon library (Lucide-style, 20x20, stroke 1.8) ----------------------
const ICONS = {
  activity:  `<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>`,
  clipboard: `<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M16 4h2a2 2 0 012 2v14a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/></svg>`,
  lock:      `<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>`,
  alert:     `<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`,
  eye:       `<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>`,
  target:    `<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>`,
  shield:    `<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>`,
  bell:      `<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 01-3.46 0"/></svg>`,
  search:    `<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>`,
  globe:     `<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z"/></svg>`,
  user:      `<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`,
  building:  `<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="1"/><path d="M16 22V12H8v10"/><path d="M9 7h1"/><path d="M14 7h1"/><path d="M9 11h1"/><path d="M14 11h1"/></svg>`,
  arrow:     `<svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>`,
};

// -- Field tooltip copy — keyed by field id ----------------------------------
const FIELD_TOOLTIPS = {
  // ── Shared fields ──
  firm_name: 'The full legal name of your FCA-authorised firm exactly as it appears on the FCA Register. Used to identify the firm across all sections of the report.',
  frn: 'Your Firm Reference Number assigned by the FCA. Verify it at register.fca.org.uk. Leave blank if the firm is not yet authorised.',
  assessment_period: 'The time window this assessment covers, e.g. "Q3 2026" or "1 Jan – 30 Jun 2026". All findings and reconciliation checks are scoped to this period.',

  // ── CASS Health Check ──
  cass_category: 'CASS firm size. Small: client money under £1m; Medium: £1m–£1bn; Large: over £1bn or custody assets over £10bn. Category determines supervision intensity and reconciliation frequency under CASS 7.13.',
  last_cm_reconciliation_date: 'Date of the most recent internal client money reconciliation. CASS 7.13.4R requires daily reconciliation for most firms. An overdue reconciliation is one of the most common FCA enforcement triggers.',
  last_custody_reconciliation_date: 'Date of the most recent custody asset reconciliation. CASS 6.6.5R requires firms to reconcile custody records promptly after each business day or after each transaction.',
  client_money_calculation_method: 'Standard Method: the firm calculates the required client money resource each business day (CASS 7.13.4R). Alternative Method: an FCA-approved shortcut typically used by retail-facing firms (CASS 7.13.8R).',
  alternative_method_fca_agreed: 'If you use the Alternative Calculation Method, the FCA must have formally agreed to this in writing before you adopt it. Using it without FCA sign-off is itself a CASS 7 breach.',
  max_single_institution_percentage: 'The highest percentage of total client money held at any single approved bank. CASS 7.13.6R requires diversification — concentrations above 20% need documented justification.',
  custody_assets_segregated: 'Whether client custody assets are held in accounts clearly designated as client accounts, entirely separate from the firm\'s own assets. Segregation is the foundation of CASS 6.',
  acknowledgement_letters_in_place: 'Banks and third-party custodians must sign acknowledgement letters confirming they hold assets or money on a client basis and will not set off the firm\'s own debts against them. Required by CASS 7.18.2R and CASS 6.4.',
  coof_individual_named: 'The CASS Operational Oversight Function (COOF) requires a specific named individual to hold responsibility for CASS oversight. Under SM&CR this maps to a Senior Manager Prescribed Responsibility.',
  coof_last_review_date: 'Date the COOF last formally reviewed CASS compliance. The FCA expects documented periodic reviews — at minimum annually, more frequently for large or complex firms.',
  cass_breaches_last_12_months: 'Whether any CASS rule breaches occurred in the last 12 months. All CASS breaches must be reported to the FCA promptly under CASS 10.2 and CASS 7.6.17R — even resolved breaches must be disclosed.',
  has_retail_clients: 'Whether the firm holds client money for retail clients as defined under MiFID II / COBS 3. Retail client status triggers additional obligations including the CASS 7.11.32R interest payment rule (effective 25 September 2026).',
  retail_interest_paid: 'New rule CASS 7.11.32R (effective 25 September 2026): firms MUST pay interest on client money held for retail clients unless the client has expressly opted out. Non-compliance is a CASS breach even without a client complaint.',
  custodian_selection_grounds_recorded: 'New rule CASS 6.3.2A R (2026): firms must maintain a written record of the specific grounds for selecting each third-party custodian, demonstrating proper due diligence was conducted at selection and on an ongoing basis.',
  is_payment_or_emoney_firm: 'Payment institutions and e-money institutions are governed by CASS 15, not CASS 6 or 7. CASS 15 introduced a new safeguarding regime effective 7 May 2026 with specific rules on safeguarding methods, reconciliation, and auditor confirmation.',
  cass_breach_details: 'Describe each CASS breach: rule breached, date discovered, cause (systems / process / human error), whether self-reported to the FCA, and remediation taken. Drives the breach severity scoring section of the report.',

  // ── CASS Resolution Pack ──
  crp_document_exists: 'A CASS Resolution Pack (CRP) must exist as a document or set of documents enabling an insolvency administrator to identify and return client assets within 48 hours. Required by CASS 10.2.2R.',
  crp_accessible_48hrs: 'CASS 10.2.2R requires the resolution pack to be retrievable within 48 hours of the firm entering insolvency. It must be stored outside any systems an administrator could freeze.',
  crp_responsible_individual: 'The named individual responsible for maintaining the resolution pack and producing it on demand. This responsibility should be mapped to an SM&CR Prescribed Responsibility.',
  crp_last_review_date: 'The CRP must be reviewed and updated after any material business change, and at minimum annually. A stale pack is an FCA finding and may fail the 48-hour retrieval test.',
  crp_tested: 'Whether the firm has evidence that it tested the CRP\'s retrieval within the 48-hour window. FCA expects documented testing with outcomes recorded — existence of the pack alone is insufficient.',
  crp_last_test_date: 'Date of the most recent CRP retrieval drill. FCA expects periodic testing to demonstrate the pack can actually be retrieved and used under insolvency conditions.',
  crp_secure_offsite_storage: 'The CRP must be stored where it remains accessible in the event of insolvency — ideally off-site, in a third-party system, or with a trusted adviser. Cloud storage secured against the firm\'s own credentials is acceptable.',
  client_asset_schedule: 'A schedule listing all client assets held by the firm in sufficient detail for an administrator to identify each asset, its owner, and its location. A core component of the CRP under CASS 10.2.2R.',
  acknowledgement_letters: 'Copies of all current CASS acknowledgement letters from banks, custodians, and third-party agents must be included in the CRP. Without these an insolvency administrator cannot freeze or transfer the assets.',
  reconciliation_records: 'Recent reconciliation records must be included so an administrator can verify holdings match client entitlements. CASS 10.2.2R specifies the minimum content required.',
  system_access_credentials: 'Documented instructions for how an insolvency administrator could access the firm\'s client asset record-keeping systems, including system names, login paths, and IT contact details.',

  // ── Client Money Segregation ──
  calculation_method: 'The method used to calculate the required client money resource daily. Standard Method (CASS 7.13.4R) and Alternative Method (CASS 7.13.8R) have different data and frequency requirements.',
  last_internal_reconciliation_date: 'Date of the most recent internal client money reconciliation (firm\'s books vs. what the firm believes it holds). Under CASS 7.13.4R this must be performed each business day.',
  internal_reconciliation_frequency: 'How often internal client money reconciliations are performed. Daily is required under CASS 7.13.4R for the Standard Method. Less frequent reconciliation is a CASS breach unless using the Alternative Method with FCA agreement.',
  last_external_reconciliation_date: 'Date of the most recent external reconciliation (firm records vs. bank or third-party statements). Must be performed promptly after statements are received — at minimum monthly.',
  max_single_institution_pct: 'The highest percentage of total client money held at any single approved bank. CASS 7.13.6R requires diversification — concentrations above 20% require documented justification.',
  acknowledgement_letters_all_accounts: 'Whether acknowledgement letters are in place for every account where client money is held. A missing letter for any account is a CASS 7.18 breach.',
  all_accounts_designated: 'Whether every account holding client money is clearly designated as a client account in its title and in the firm\'s records. CASS 7.13.2R requires accounts to be identifiable as client money accounts.',
  accounts_with_affiliated_entities: 'Whether any client money is held in accounts at group companies or affiliated entities. This requires specific FCA permission and enhanced disclosure to clients under CASS 7.13.10R.',
  third_party_agent_arrangements: 'Whether the firm passes client money to a third-party agent for holding. This requires a written agreement, acknowledgement letters, and ongoing due diligence on the agent under CASS 7.13.12R.',
  reconciliation_breaks_identified: 'Whether the most recent reconciliation identified any breaks (differences between the firm\'s books and amounts held at banks). Even small breaks require investigation and documentation.',
  break_details: 'Describe any reconciliation breaks: the amount, which account, date identified, cause (timing difference, system error, missing deposit, etc.), and whether resolved. Unresolved breaks are scored RED.',

  // ── CASS Breach Log ──
  breach_register_maintained: 'CASS 7.6.17R requires firms to maintain a written record of every CASS breach, including remediated ones. The register is a primary FCA inspection document and must be kept current.',
  breach_date: 'The date the CASS breach first occurred or was first identified. This drives the FCA notification timeline — firms must notify the FCA promptly after identifying a material breach.',
  breach_type: 'The category of breach. Segregation failures (CASS 7) and custody failures (CASS 6) are most common. Reporting failures relate to breaches of CASS 7.6.17R or CASS 10 obligations.',
  rule_breached: 'The specific FCA Handbook rule that was breached, e.g. "CASS 7.13.4 R". Use the exact reference — this determines which remediation guidance and scoring criteria apply in the report.',
  fca_notified: 'Whether the FCA has been formally notified of this breach. Material CASS breaches must be reported promptly under FCA SUP 15.3.1R. Failing to notify when required is itself a separate breach.',
  notification_required: 'Whether this breach meets the threshold for mandatory FCA notification under SUP 15.3.1R. All CASS breaches resulting in client detriment or exceeding the materiality threshold must be notified.',
  notification_date: 'The date the FCA was notified. The FCA expects prompt notification as soon as the firm becomes aware of a material breach, with a full report to follow within a reasonable period.',
  remediation_status: 'Current remediation state. Open: root cause not yet resolved. Monitoring: fix in place but firm is watching for recurrence. Closed: fully remediated with evidence.',
  root_cause_analysis: 'Why the breach occurred: process failure, system error, human error, governance gap, etc. The FCA expects a genuine root cause analysis — not just a description of symptoms. Drives the remediation quality score.',

  // ── CASS Oversight (COOF) ──
  coof_individual_name: 'Full name of the individual appointed to the CASS Operational Oversight Function. This person holds personal responsibility for the firm\'s CASS oversight programme under CASS 1A.3 and SM&CR.',
  coof_individual_qualified: 'Whether the COOF individual has relevant qualifications, experience, or training for the role. The FCA expects the individual to be competent under FIT 2.1 — no specific qualification is mandated.',
  coof_also_compliance_officer: 'Whether the COOF role is held by the same person as the Compliance Officer. This is permitted but concentrates oversight responsibilities — the report will flag this as a governance observation.',
  last_coof_review_of_cass_date: 'Date the COOF last conducted a formal CASS compliance review. CASS 1A.3 requires regular documented reviews — at minimum annually for large firms.',
  last_coof_report_to_board_date: 'Date the COOF last presented a formal report to the board or governing body. Board-level CASS reporting is an FCA expectation tested on inspections.',
  board_minutes_confirm_coof_report: 'Whether board minutes evidencing receipt and discussion of the COOF report exist. FCA inspectors expect written evidence — verbal briefings are insufficient.',
  outstanding_coof_recommendations: 'List any COOF recommendations not yet implemented. Persistent outstanding recommendations indicate a breakdown between oversight and governance — an FCA red flag.',

  // ── Threat Intelligence ──
  business_lines: 'The firm\'s main activities: Retail Banking, Wealth Management, Custody, etc. This determines which threat typologies — fraud, insider risk, CASS-specific attacks — are most relevant to include.',
  geographic_footprint: 'Countries or regions where the firm operates, holds clients, or transacts. Cross-border presence affects sanctions exposure, AML risk, and the relevance of specific threat actor profiles.',

  // ── Cyber Threat Assessment ──
  cbest_assessment_completed: 'CBEST is the Bank of England\'s intelligence-led cyber resilience testing framework. Completion signals advanced cyber maturity and is positively weighted by the FCA.',
  last_cbest_date: 'Date of the most recent CBEST or TIBER-UK assessment. In-scope firms are expected to retest periodically (typically every 3 years) as the threat landscape evolves.',
  ibs_identified: 'Whether the firm has formally documented its Important Business Services (IBS) as defined under FCA PS21/3. All FCA-regulated firms must have identified their IBS and set impact tolerances.',
  impact_tolerances_set: 'Whether the firm has set maximum tolerable disruption levels (impact tolerances) for each IBS. Tolerances must be outcome-focused — measurable and time-based. Required under FCA PS21/3.',
  scenario_testing_completed: 'Whether the firm has completed severe-but-plausible operational disruption scenario testing against its IBS impact tolerances. Annual testing is expected under FCA PS21/3.',
  mfa_on_critical_systems: 'Whether multi-factor authentication is enforced on all critical and privileged systems. MFA is the single most effective control against credential-based attacks and is a baseline FCA supervisory expectation.',
  privileged_access_management: 'Whether the firm has a formal PAM programme controlling administrative and elevated access rights. Uncontrolled privileged access is one of the most common causes of material data breaches.',
  cyber_incident_response_plan_exists: 'Whether the firm has a documented cyber incident response plan covering detection, containment, notification, and recovery. Required under SYSC 13 and tested under FCA PS21/3.',
  cyber_response_plan_tested: 'Whether the cyber incident response plan has been tested through tabletop exercise or simulation. Untested plans are scored AMBER — firms cannot demonstrate they would work under real pressure.',
  third_party_cyber_risk_assessed: 'Whether the firm has assessed cyber risk from critical third-party suppliers and outsourcers. FCA PS26/2 introduces enhanced third-party operational incident reporting requirements from March 2027.',

  // ── FCA Incident Response ──
  incident_type: 'The category of incident. Determines notification obligations: CASS breaches (CASS 7.6.17R), cyber incidents (SYSC 13), data breaches (UK GDPR Article 33), operational failures (PS26/2).',
  incident_datetime: 'Date and time the incident first occurred or was first identified. The FCA notification clock starts from identification — not from when the root cause is understood.',
  fca_notification_datetime: 'Date and time the FCA was formally notified. PS26/2 requires notification within 24 hours of identifying a material operational incident. CASS breaches under SUP 15.3.1R must be reported "promptly".',
  fca_notification_reference: 'The reference number provided by the FCA when the notification was submitted via FCA Connect or RegData. Keep for all follow-up correspondence.',
  ico_notified: 'Whether the Information Commissioner\'s Office (ICO) was notified. UK GDPR Article 33 requires notification within 72 hours of identifying a personal data breach. Failure to notify is a separate breach.',
  incident_contained: 'Whether the immediate threat has been contained — no further client data at risk, systems isolated, or breach source closed. Containment is distinct from full remediation.',
  containment_date: 'Date the incident was contained. Time-to-containment is a key metric in FCA and ICO assessments of the firm\'s incident response capability.',
  clients_affected: 'The number of clients whose data, assets, or service were affected. Drives materiality thresholds for FCA notification and Consumer Duty impact assessment obligations.',
  client_assets_affected: 'Whether client money or custody assets were affected. Any CASS shortfall must be immediately made good, and the breach separately reported under CASS rules.',
  client_assets_amount: 'Approximate value of client assets affected. Determines whether the incident meets the materiality threshold for FCA Consumer Duty remediation obligations.',
  root_cause: 'Identified or suspected root cause: technical vulnerability, process failure, human error, third-party failure. Honest root cause analysis is expected by the FCA and drives remediation quality scoring.',
  timeline: 'Chronological log of key events: when the incident started, when detected, when internal teams were alerted, when clients were affected, and when containment actions were taken.',
  lessons_learned: 'What the firm has identified as lessons. The FCA expects a genuine learning exercise — not a box-tick — that leads to documented control improvements.',
  remediation_actions: 'Specific actions being taken to fully remediate the incident: system patches, process changes, retraining, policy updates. Include owners and target completion dates.',

  // ── Due Diligence ──
  subject_name: 'Full legal name of the entity or individual subject to due diligence. For companies use the exact registered name; for individuals use full legal name including middle names.',
  subject_type: 'Category of the subject. Custodians require CASS 6 compliance checks; Senior Managers require FIT/COCON assessments; suppliers require contract and financial stability checks.',
  purpose: 'The commercial reason for conducting due diligence, e.g. "New third-party custodian appointment" or "SMF approval application". Drives the scope of checks required.',
  fca_frn_or_irn: 'The FCA Firm Reference Number (FRN) for authorised firms, or Individual Reference Number (IRN) for approved individuals. Used to verify FCA Register status and check enforcement history.',
  fca_registration_required: 'Whether FCA authorisation is required for this entity or individual to carry out the proposed activities. Engaging an unregistered firm in regulated activities is a criminal offence.',
  fca_registered: 'Whether the subject appears on the FCA Register as currently authorised. Always verify directly at register.fca.org.uk — do not rely on the subject\'s own representations.',
  supplier_fca_authorised: 'Whether the supplier holds the relevant FCA authorisation for the services being provided. Some outsourced functions (e.g. custody, client money holding) require the supplier to hold specific FCA permissions.',
  written_agreement_in_place: 'Whether a formal written agreement governs the arrangement. For CASS-related outsourcing, a written agreement is mandatory under CASS 7.13.12R (third-party agents) and CASS 6.3.3R (custodians).',
  sanctions_match: 'Whether the subject appears on any UK (OFSI), EU, or US (OFAC/SDN) sanctions list. A positive match must be reported to OFSI immediately and all dealings suspended.',
  criminal_convictions: 'Whether the individual has any criminal convictions relevant to financial services. Material under FCA FIT 2.1 (honesty and integrity) for all Senior Manager approval applications.',
  ccjs_or_bankruptcy: 'Whether the individual has unsatisfied County Court Judgements or a history of personal bankruptcy. Material under FCA FIT 2.2 (financial soundness) for Senior Manager approvals.',
  prior_regulatory_actions: 'Whether the individual or firm has been subject to regulatory actions by the FCA, PRA, or overseas regulators. Prior enforcement history must be disclosed in FCA applications.',
  active_fca_ban_or_prohibition: 'Whether the FCA has issued a current prohibition order against this individual or firm. Engaging a prohibited person in a regulated activity is a criminal offence. Check the FCA Warning List and Register.',
  professional_qualifications_verified: 'Whether claimed professional qualifications have been verified with the issuing body. False qualification claims are a fitness and propriety concern under FCA FIT 2.1.',

  // ── Country Risk ──
  country: 'The jurisdiction being assessed. Determines applicable sanctions regimes (UK/OFSI, EU, UN, US/OFAC), FATF status, AML risk rating, and FCA prior concerns about local custody arrangements.',
  sanctions_applicable: 'Whether UK (OFSI), EU, UN, or US (OFAC) sanctions regimes restrict transactions with this country or its nationals. A "Yes" triggers Enhanced Due Diligence and OFSI notification obligations.',
  fatf_grey_list: 'Whether the country is on the FATF Grey List (increased monitoring) or Black List (call for action). FATF status is incorporated into UK AML regulations (POCA 2002 / MLR 2017) and triggers Enhanced Due Diligence.',
  corruption_perceptions_index_score: 'The Transparency International Corruption Perceptions Index score from 0 (highly corrupt) to 100 (very clean). Used to calibrate the AML risk rating — scores below 40 indicate high-risk jurisdictions.',
  political_stability: 'Assessment of the country\'s political stability. Unstable or Failed State designations significantly increase the risk of asset freezes, regulatory non-recognition, and inability to repatriate client assets.',
  fca_prior_concern: 'Whether the FCA has previously expressed supervisory concerns about this jurisdiction — e.g. through Dear CEO letters, supervisory notices, or enforcement actions involving local custody arrangements.',

  // ── Executive Protection (SM&CR) ──
  subject_role: 'The subject\'s job title and role. Determines which SMF functions and Prescribed Responsibilities apply under SM&CR, and the level of public exposure relevant to protection planning.',
  smf_functions: 'Specific Senior Management Function (SMF) designations held, e.g. "SMF1 (CEO), SMF16 (Compliance Oversight)". Each SMF carries defined legal accountability under FSMA 2000 and the Senior Managers Regime.',
  public_profile_level: 'The individual\'s public visibility. High means regular media appearances or prominent social media presence. Higher profiles create greater reputational risk, targeting risk, and disinformation exposure.',
  international_travel_frequency: 'How often the individual travels internationally. Frequent travel to high-risk jurisdictions materially increases kidnap and ransom, surveillance, and device compromise risk.',
  travel_destinations: 'Countries or regions regularly visited. Destinations under FCO travel advisories, sanctions regimes, or with active hostile intelligence service activity require enhanced protective protocols.',
  home_working: 'Whether the individual regularly works from home. Home environments typically have weaker physical and cyber security than corporate offices, creating additional data exfiltration and physical access risks.',
  known_threats_or_incidents: 'Whether there are known or reported threats against this individual, including previous security incidents or stalking. Prior incidents significantly increase the current risk rating.',
  harassment_or_protest_targeting: 'Whether the individual or their firm is subject to organised protest, activist targeting, or media harassment. Increasingly relevant for ESG-exposed financial services executives.',
  digital_footprint_concerns: 'Whether the individual has a digital footprint that creates material risk — excessive personal information publicly available, location data disclosed on social media, or prior data breach exposure.',
  protective_measures_in_place: 'Describe existing measures: personal protection, secure transport, residence security, device encryption, social media monitoring, cyber hygiene training, etc.',

  // ── Physical Security ──
  premises_type: 'The type of premises being assessed. Data centres require higher access controls and environmental monitoring; vaults require standards such as BS EN 1143. Each type has different scoring criteria.',
  address: 'Full address of the premises. Used to contextualise the local threat environment: crime statistics, proximity to critical infrastructure, and natural hazard (flood, fire) exposure.',
  access_control_in_place: 'Whether an electronic or physical access control system is operational. Access control is a baseline FCA operational resilience requirement and an NPSA/CPNI standard for critical infrastructure sites.',
  access_control_type: 'The technology used: proximity fob, biometric (fingerprint, iris, facial recognition), PIN pad, or combination. Biometric systems provide stronger non-repudiation and are preferred for server rooms and vaults.',
  cctv_coverage: 'Whether CCTV surveillance is in place. CCTV is a primary deterrence and forensic evidence tool. FCA operational resilience expectations and most insurer requirements mandate coverage of all access points.',
  cctv_areas_covered: 'Areas covered by CCTV. Minimum expected coverage includes all entry/exit points, server rooms, trading floors, and cash handling areas. Gaps are recorded as findings.',
  intruder_alarm: 'Whether an electronic intruder alarm is installed. Alarms should be monitored 24/7 by a certificated Alarm Receiving Centre (ARC) under BS EN 50131 to meet insurance and FCA operational resilience standards.',
  alarm_standard: 'Technical standard to which the alarm is installed: PD 6662 (UK), BS 8243, or BS EN 50131. FCA-regulated firms and most insurers require a recognised standard for insurance cover validity.',
  security_personnel_on_site: 'Whether SIA-licensed security personnel are present on site. On-site security is expected for head offices, data centres, and trading floors handling significant client assets.',
  security_hours: 'Hours when security personnel are present. Coverage gaps (nights, weekends) represent periods of elevated risk and should be compensated by technology-based monitoring and alarm systems.',
  perimeter_security: 'Whether physical perimeter controls (fencing, barriers, vehicle hostile mitigation) are in place. NPSA/CPNI standards recommend measures proportionate to the criticality of the site.',
  visitor_management_process: 'Whether a formal visitor management process exists: pre-registration, identity verification, escort policy, visitor badges, and access logging. Inadequate visitor management is a common audit finding.',
  secure_document_disposal: 'Whether there is a documented process for disposing of sensitive documents: cross-cut shredding, certified destruction, or secure disposal bins. Required under UK GDPR and FCA data security expectations.',
  business_continuity_plan_for_premises: 'Whether a BCP exists for this premises, covering loss of access, fire, flood, or infrastructure failure. Required under FCA PS21/3 for sites supporting Important Business Services.',
  last_physical_security_review_date: 'Date of the most recent formal physical security audit of this premises. Annual reviews are the minimum FCA operational resilience expectation.',
  prior_incidents: 'Previous security incidents at these premises: break-ins, tailgating, theft, violence, or data removal. Prior incidents significantly affect the current risk score.',
  prior_incidents_remediated: 'Whether prior security incidents have been fully investigated and remediated. Unresolved prior incidents are scored RED — they indicate systemic weaknesses that remain exploitable.',

  // ── FATF Blacklist Intelligence Report ──
  counterparty_name: 'Full legal name of the counterparty, client, or entity subject to this FATF assessment. For natural persons use the full legal name; for companies use the exact registered name.',
  counterparty_type: 'The nature of the relationship being assessed. Type determines which ML/TF typology risks apply and which specific MLR 2017 provisions govern the relationship.',
  client_category: 'Risk category of the client. PEPs, charities/NPOs, and high-net-worth individuals attract enhanced obligations under MLR 2017 Regs 35–36.',
  transaction_type: 'The type of transaction or activity being assessed. Trade finance, correspondent banking, and payment processing each carry distinct FATF-identified ML/TF risks.',
  countries_involved: 'All countries connected to this transaction or relationship — counterparty domicile, beneficial owner nationality, source of funds origin, and correspondent bank locations. Separate multiple countries with commas.',
  edd_procedures_in_place: 'Whether Enhanced Due Diligence procedures have been applied for this relationship, as required by MLR 2017 Reg 33 for any connection to a high-risk third country listed by FATF.',
  sanctions_screening_tool: 'The name of the sanctions screening system used (e.g. WorldCheck, Accuity, Comply Advantage). FCA expects firms to name their screening tool in compliance documentation.',
  sanctions_screening_performed: 'Whether a current sanctions screening has been performed against UK (OFSI), EU, UN, and US (OFAC/SDN) lists. Screening must be performed at onboarding and monitored on an ongoing basis.',
  pep_screening_performed: 'Whether Politically Exposed Person screening has been performed for all principals, directors, and beneficial owners, as required by MLR 2017 Reg 35.',
  adverse_media_screening: 'Whether an adverse media / negative news search has been conducted. FCA Financial Crime Guide expects firms to check for negative news at onboarding and on an ongoing basis for higher-risk customers.',
  sar_filing_required: 'Whether the facts of this relationship or transaction give rise to an obligation to file a Suspicious Activity Report with the National Crime Agency (NCA) under POCA 2002 s330.',
  sar_filed: 'Whether a Suspicious Activity Report has been filed with the NCA. If an obligation exists, failure to file is a criminal offence under POCA 2002 s330. Filing after the suspicion arises is preferred — do not tip off the customer.',
  source_of_funds_verified: 'Whether the source of funds (and source of wealth for high-risk customers) has been verified with documentary evidence. Essential for all high-risk jurisdiction relationships under MLR 2017 Reg 28(9).',
  beneficial_owner_identified: 'Whether the ultimate beneficial owner(s) holding ≥25% ownership or control have been identified and verified. Required by MLR 2017 Reg 5 and reinforced by the Economic Crime Act 2022.',
  aml_training_completion_rate: 'The percentage of relevant staff who have completed current AML/CFT training. Benchmark is ≥90%. MLR 2017 Reg 24 requires firms to ensure all staff receive regular AML awareness training.',
  last_aml_risk_assessment_date: 'Date the firm last completed a formal firm-wide AML/CFT risk assessment under MLR 2017 Reg 18. Must be reviewed and updated annually or after material changes to the business model or risk profile.',
  correspondent_bank_relationships: 'Whether the firm maintains any correspondent banking relationships in connection with this transaction or jurisdiction. Correspondent banking relationships require enhanced due diligence under MLR 2017 Reg 34.',
  correspondent_bank_in_listed_jurisdiction: 'Whether any correspondent bank in this arrangement is domiciled in or supervised by a FATF-listed jurisdiction. If yes, enhanced due diligence with senior management approval is mandatory under MLR 2017 Reg 34.',
  shell_bank_check_performed: 'Whether the firm has verified that no correspondent bank in this arrangement is a shell bank (i.e. lacks genuine physical presence in any jurisdiction and is not subject to AML supervision). Correspondent relationships with shell banks are prohibited under MLR 2017 Reg 34(3).',

  // ── GRC Intelligence Report ──
  grc_platform_in_use: 'Whether the firm uses a dedicated GRC technology platform (e.g. ServiceNow GRC, MetricStream, LogicGate). The FCA expects technology-enabled governance for regulated firms — manual-only GRC is scored AMBER or RED depending on size.',
  governance_board_oversight: 'Whether the board exercises active oversight of the GRC programme, with regular reporting, challenge, and individual accountability. FCA expects evidence of board-level GRC ownership under SM&CR.',
  governance_policy_doc_current: 'Whether governance policies (risk, compliance, CASS, SM&CR) have been reviewed within the last 12 months and updated for 2026 regulatory changes.',
  governance_policy_comprehension_rate: 'The percentage of staff who have read, understood, and attested to relevant policies. Benchmark is ≥85%. Low comprehension rates indicate inadequate policy communication and are scored AMBER.',
  governance_decision_framework: 'Whether the firm has a documented decision-making framework — escalation pathways, delegation of authority, and accountability mapping. Required under SM&CR to demonstrate governance adequacy.',
  risk_appetite_defined: 'Whether the firm has a formally documented and board-approved risk appetite statement defining the types and levels of risk it is willing to accept. Missing risk appetite is an automatic AMBER finding.',
  risk_register_maintained: 'Whether the firm maintains an active risk register documenting identified risks, ratings, owners, and treatment plans. A fundamental GRC tool expected by the FCA.',
  risk_register_last_reviewed: 'Date the risk register was last reviewed and updated. Registers should be reviewed at minimum quarterly and immediately after material business change, incidents, or regulatory updates.',
  risk_open_items: 'Total number of risks currently open (not yet fully treated or accepted). Benchmark is ≤15. Excessive open items suggest inadequate risk governance capacity.',
  risk_critical_items: 'Number of CRITICAL or HIGH risks open beyond their resolution target date. More than one overdue critical item triggers AMBER — escalation to the Risk Committee is expected.',
  risk_identification_process: 'Whether the firm has a formal, documented process for identifying new and emerging risks — e.g. quarterly workshops, horizon scanning, control self-assessments. Ad hoc identification is scored AMBER.',
  third_party_risk_assessed: 'Whether the firm has formally assessed risk from critical third-party providers (cloud, outsourcers, custodians). FCA PS26/2 introduces enhanced third-party risk requirements from March 2027.',
  compliance_regulatory_monitoring: 'Whether an active process for monitoring FCA regulatory changes, policy statements, and consultation papers exists. Missing a material change is a compliance failure under SYSC 6.1.',
  compliance_training_completion_rate: 'Percentage of staff who have completed mandatory compliance training (CASS, SM&CR, AML, Consumer Duty). Benchmark is ≥90%. Non-completion is an individual conduct issue under COCON.',
  compliance_control_effectiveness: 'The assessed percentage of key controls operating effectively, based on testing results (not self-certification). Benchmark is ≥80%. Calculated from internal audit or control testing output.',
  compliance_audit_findings_open: 'Number of internal or external audit findings not yet implemented. Benchmark is ≤5. Persistent open findings indicate weak accountability and poor governance discipline.',
  fca_regulatory_changes_tracked: 'Whether all material FCA regulatory changes relevant to the firm\'s activities have been identified and mapped to implementation plans — including SM&CR Phase 1, CASS 7.11.32R, CASS 6.3.2A R, and PS26/2.',
};

// -- Report catalogue --------------------------------------------------------
const REPORTS = [
  {
    id: 'cass_health_check',
    title: 'CASS Health Check',
    tag: 'CASS 6 & 7',
    tagClass: 'tag-cass',
    iconClass: 'cat-cass',
    icon: 'activity',
    desc: 'Reconciliation gaps, pool compliance, CASS 7.13.4R & 7.18 scoring with RAG output.',
    regs: 'CASS 6 - CASS 7 - CASS 7A',
    fields: [
      { row: 'cols-2', fields: [
        { id: 'firm_name', label: 'Firm Name', type: 'text', placeholder: 'Barclays Bank plc', required: true },
        { id: 'frn', label: 'FCA FRN', type: 'text', placeholder: '122702' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'cass_category', label: 'CASS Firm Category', type: 'select', options: ['Small', 'Medium', 'Large'] },
        { id: 'assessment_period', label: 'Assessment Period', type: 'text', placeholder: 'e.g. Q3 2026' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'last_cm_reconciliation_date', label: 'Last Client Money Recon Date', type: 'date' },
        { id: 'last_custody_reconciliation_date', label: 'Last Custody Recon Date', type: 'date' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'client_money_calculation_method', label: 'CM Calculation Method', type: 'select', options: ['Standard', 'Alternative'] },
        { id: 'alternative_method_fca_agreed', label: 'Alternative Method FCA Agreed?', type: 'select', options: ['false', 'true'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'max_single_institution_percentage', label: 'Max Single Institution %', type: 'number', placeholder: '20' },
        { id: 'custody_assets_segregated', label: 'Custody Assets Segregated?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'acknowledgement_letters_in_place', label: 'Acknowledgement Letters in Place?', type: 'select', options: ['true', 'false'] },
        { id: 'coof_individual_named', label: 'COOF Individual Named?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'coof_last_review_date', label: 'COOF Last Review Date', type: 'date' },
        { id: 'cass_breaches_last_12_months', label: 'CASS Breaches in Last 12 Months?', type: 'select', options: ['false', 'true'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'has_retail_clients', label: 'Has Retail Clients?', type: 'select', options: ['true', 'false'] },
        { id: 'retail_interest_paid', label: 'Retail Interest Paid? (CASS 7.11.32R)', type: 'select', options: ['true', 'false', ''] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'custodian_selection_grounds_recorded', label: 'Custodian Selection Grounds Recorded? (CASS 6.3.2A R)', type: 'select', options: ['true', 'false'] },
        { id: 'is_payment_or_emoney_firm', label: 'Payment / E-Money Firm? (CASS 15)', type: 'select', options: ['false', 'true'] },
      ]},
      { row: null, fields: [
        { id: 'cass_breach_details', label: 'Breach Details (if any)', type: 'textarea', placeholder: 'Describe any CASS breaches in the period...', rows: 3 },
      ]},
    ],
  },
  {
    id: 'cass_resolution_pack',
    title: 'CASS Resolution Pack Readiness',
    tag: 'CASS 10',
    tagClass: 'tag-cass',
    iconClass: 'cat-cass',
    icon: 'clipboard',
    desc: 'Client asset return readiness under CASS 10 -- pack completeness, distribution, nominee companies.',
    regs: 'CASS 10 - FCA SUP',
    fields: [
      { row: 'cols-2', fields: [
        { id: 'firm_name', label: 'Firm Name', type: 'text', required: true },
        { id: 'frn', label: 'FCA FRN', type: 'text' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'crp_document_exists', label: 'Resolution Pack Exists?', type: 'select', options: ['true', 'false'] },
        { id: 'crp_accessible_48hrs', label: 'Retrievable within 48 Hours?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'crp_responsible_individual', label: 'Responsible Individual', type: 'text', placeholder: 'Name of pack owner' },
        { id: 'crp_last_review_date', label: 'Last Review Date', type: 'date' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'crp_tested', label: 'Pack Tested?', type: 'select', options: ['true', 'false'] },
        { id: 'crp_last_test_date', label: 'Last Test Date', type: 'date' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'crp_secure_offsite_storage', label: 'Secure Off-Site Storage?', type: 'select', options: ['true', 'false'] },
        { id: 'client_asset_schedule', label: 'Client Asset Schedule Included?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'acknowledgement_letters', label: 'Acknowledgement Letters Included?', type: 'select', options: ['true', 'false'] },
        { id: 'reconciliation_records', label: 'Reconciliation Records Included?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: null, fields: [
        { id: 'system_access_credentials', label: 'System Access Credentials Documented?', type: 'select', options: ['true', 'false'] },
      ]},
    ],
  },
  {
    id: 'client_money_segregation',
    title: 'Client Money Segregation Audit',
    tag: 'CASS 7',
    tagClass: 'tag-cass',
    iconClass: 'cat-cass',
    icon: 'lock',
    desc: 'Segregation method, CMA reconciliation, daily reconciliation compliance under CASS 7.',
    regs: 'CASS 7 - CASS 7A',
    fields: [
      { row: 'cols-2', fields: [
        { id: 'firm_name', label: 'Firm Name', type: 'text', required: true },
        { id: 'frn', label: 'FCA FRN', type: 'text' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'calculation_method', label: 'CM Calculation Method', type: 'select', options: ['Standard', 'Alternative'] },
        { id: 'alternative_method_fca_agreed', label: 'Alternative Method FCA Agreed?', type: 'select', options: ['false', 'true'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'last_internal_reconciliation_date', label: 'Last Internal Recon Date', type: 'date' },
        { id: 'internal_reconciliation_frequency', label: 'Internal Recon Frequency', type: 'select', options: ['Daily', 'Weekly', 'Monthly'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'last_external_reconciliation_date', label: 'Last External Recon Date', type: 'date' },
        { id: 'max_single_institution_pct', label: 'Max Single Institution %', type: 'number', placeholder: '20' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'acknowledgement_letters_all_accounts', label: 'Ack Letters for All Accounts?', type: 'select', options: ['true', 'false'] },
        { id: 'all_accounts_designated', label: 'All Accounts Designated?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'accounts_with_affiliated_entities', label: 'Accounts with Affiliated Entities?', type: 'select', options: ['false', 'true'] },
        { id: 'third_party_agent_arrangements', label: 'Third-Party Agent Arrangements?', type: 'select', options: ['false', 'true'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'reconciliation_breaks_identified', label: 'Reconciliation Breaks Found?', type: 'select', options: ['false', 'true'] },
      ]},
      { row: null, fields: [
        { id: 'break_details', label: 'Break Details (if any)', type: 'textarea', placeholder: 'Describe any reconciliation breaks found...', rows: 3 },
      ]},
    ],
  },
  {
    id: 'cass_breach_log',
    title: 'CASS Breach Log & Remediation',
    tag: 'CASS BREACH',
    tagClass: 'tag-cass',
    iconClass: 'cat-cass',
    icon: 'alert',
    desc: 'Document CASS breaches, root cause analysis, corrective actions and FCA notification status.',
    regs: 'CASS 6 - CASS 7 - FCA SUP',
    fields: [
      { row: 'cols-2', fields: [
        { id: 'firm_name', label: 'Firm Name', type: 'text', required: true },
        { id: 'frn', label: 'FCA FRN', type: 'text' },
      ]},
      { row: null, fields: [
        { id: 'breach_register_maintained', label: 'Breach Register Maintained?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'breach_date', label: 'Breach Date', type: 'date', required: true },
        { id: 'breach_type', label: 'Breach Type', type: 'select', options: ['CASS 7 Segregation Failure', 'CASS 6 Custody Failure', 'Reconciliation Failure', 'Reporting Failure', 'Other'] },
      ]},
      { row: null, fields: [
        { id: 'rule_breached', label: 'Rule Breached', type: 'text', placeholder: 'e.g. CASS 7.13.4 R', required: true },
      ]},
      { row: 'cols-2', fields: [
        { id: 'fca_notified', label: 'FCA Notified?', type: 'select', options: ['false', 'true'] },
        { id: 'notification_required', label: 'Notification Required?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: null, fields: [
        { id: 'notification_date', label: 'FCA Notification Date', type: 'date' },
      ]},
      { row: null, fields: [
        { id: 'remediation_status', label: 'Remediation Status', type: 'select', options: ['Open', 'Closed', 'Monitoring'] },
      ]},
      { row: null, fields: [
        { id: 'root_cause_analysis', label: 'Root Cause Analysis', type: 'textarea', placeholder: 'What caused the breach and what has been done?', rows: 3 },
      ]},
    ],
  },
  {
    id: 'cass_oversight',
    title: 'CASS Oversight (COOF)',
    tag: 'COOF',
    tagClass: 'tag-cass',
    iconClass: 'cat-cass',
    icon: 'eye',
    desc: 'CASS Operational Oversight Function -- board reporting, frequency, issues raised.',
    regs: 'CASS 1A - SM&CR',
    fields: [
      { row: 'cols-2', fields: [
        { id: 'firm_name', label: 'Firm Name', type: 'text', required: true },
        { id: 'frn', label: 'FCA FRN', type: 'text' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'cass_category', label: 'CASS Firm Category', type: 'select', options: ['Small', 'Medium', 'Large'] },
        { id: 'coof_individual_name', label: 'COOF Individual Name', type: 'text', placeholder: 'Name of appointed COOF officer' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'coof_individual_qualified', label: 'COOF Individual Qualified?', type: 'select', options: ['true', 'false'] },
        { id: 'coof_also_compliance_officer', label: 'COOF Also Compliance Officer?', type: 'select', options: ['false', 'true'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'last_coof_review_of_cass_date', label: 'Last COOF Review of CASS', type: 'date' },
        { id: 'last_coof_report_to_board_date', label: 'Last COOF Report to Board', type: 'date' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'board_minutes_confirm_coof_report', label: 'Board Minutes Confirm COOF Report?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: null, fields: [
        { id: 'outstanding_coof_recommendations', label: 'Outstanding COOF Recommendations', type: 'textarea', placeholder: 'List any outstanding recommendations...', rows: 3 },
      ]},
    ],
  },
  // ── GRC Framework Reports (non-UK regions; replaces CASS suite) ──────────────
  {
    id: 'governance_control_ops',
    title: 'Governance & Control Operations',
    tag: 'GC OPS',
    tagClass: 'tag-grc',
    iconClass: 'cat-grc',
    icon: 'activity',
    desc: 'Policy governance, risk operations, incident oversight, control effectiveness — board-level GRC posture.',
    regs: 'COSO ERM - ISO 31000 - NIST CSF',
    fields: [
      { row: 'cols-2', fields: [
        { id: 'firm_name', label: 'Firm Name', type: 'text', required: true },
        { id: 'frn', label: 'Body Ref', type: 'text', placeholder: 'Regulator reference' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'assessment_period', label: 'Assessment Period', type: 'text', placeholder: 'e.g. Q3 2026' },
        { id: 'grc_framework', label: 'GRC Framework', type: 'select', options: ['COSO ERM', 'ISO 31000', 'NIST CSF', 'OCEG', 'Mixed'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'governance_board_oversight', label: 'Board Oversight Active?', type: 'select', options: ['true', 'false'] },
        { id: 'risk_appetite_defined', label: 'Risk Appetite Defined?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'governance_policy_doc_current', label: 'Policies Reviewed (12 months)?', type: 'select', options: ['true', 'false'] },
        { id: 'governance_policy_comprehension_rate', label: 'Staff Attestation Rate (%)', type: 'number', placeholder: '85' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'compliance_control_effectiveness', label: 'Control Effectiveness (%)', type: 'number', placeholder: '80' },
        { id: 'compliance_audit_findings_open', label: 'Open Audit Findings', type: 'number', placeholder: '0' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'grc_platform_in_use', label: 'GRC Platform in Use?', type: 'select', options: ['true', 'false'] },
        { id: 'governance_decision_framework', label: 'Decision Framework Documented?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: null, fields: [
        { id: 'governance_notes', label: 'Governance Notes', type: 'textarea', placeholder: 'Key findings, exceptions, escalation items...', rows: 3 },
      ]},
    ],
  },
  {
    id: 'policy_governance',
    title: 'Policy Governance',
    tag: 'POLICY GOV',
    tagClass: 'tag-grc',
    iconClass: 'cat-grc',
    icon: 'clipboard',
    desc: 'Policy inventory, review cycles, compliance gaps, board approval status and staff attestation rates.',
    regs: 'COSO ERM - ISO 31000 - FCA SYSC',
    fields: [
      { row: 'cols-2', fields: [
        { id: 'firm_name', label: 'Firm Name', type: 'text', required: true },
        { id: 'frn', label: 'Body Ref', type: 'text' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'assessment_period', label: 'Assessment Period', type: 'text', placeholder: 'e.g. Q3 2026' },
        { id: 'total_active_policies', label: 'Total Active Policies', type: 'number', placeholder: '25' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'policies_reviewed_last_12m', label: 'Policies Reviewed (Last 12m)', type: 'select', options: ['All', 'Most', 'Some', 'None'] },
        { id: 'governance_policy_comprehension_rate', label: 'Staff Attestation Rate (%)', type: 'number', placeholder: '85' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'governance_board_oversight', label: 'Board-Approved Policies?', type: 'select', options: ['true', 'false'] },
        { id: 'policy_gaps_identified', label: 'Policy Gaps Identified?', type: 'select', options: ['false', 'true'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'policy_exception_process', label: 'Exception Process in Place?', type: 'select', options: ['true', 'false'] },
        { id: 'compliance_regulatory_monitoring', label: 'Regulatory Change Monitoring?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: null, fields: [
        { id: 'policy_notes', label: 'Policy Notes', type: 'textarea', placeholder: 'Key policy gaps, upcoming reviews, exceptions...', rows: 3 },
      ]},
    ],
  },
  {
    id: 'risk_operations',
    title: 'Risk Operations',
    tag: 'RISK OPS',
    tagClass: 'tag-grc',
    iconClass: 'cat-grc',
    icon: 'activity',
    desc: 'KRI/KPI monitoring, risk register status, appetite breaches, emerging risk scanning and trend analysis.',
    regs: 'COSO ERM - ISO 31000 - NIST RMF',
    fields: [
      { row: 'cols-2', fields: [
        { id: 'firm_name', label: 'Firm Name', type: 'text', required: true },
        { id: 'frn', label: 'Body Ref', type: 'text' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'assessment_period', label: 'Assessment Period', type: 'text', placeholder: 'e.g. Q3 2026' },
        { id: 'risk_appetite_defined', label: 'Risk Appetite Statement Defined?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'risk_register_maintained', label: 'Risk Register Maintained?', type: 'select', options: ['true', 'false'] },
        { id: 'risk_register_last_reviewed', label: 'Risk Register Last Reviewed', type: 'date' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'risk_open_items', label: 'Open Risk Items', type: 'number', placeholder: '0' },
        { id: 'risk_critical_items', label: 'Critical / High Overdue Items', type: 'number', placeholder: '0' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'kri_count', label: 'KRIs Monitored', type: 'number', placeholder: '10' },
        { id: 'kri_breaches', label: 'KRI Breaches (Last Quarter)', type: 'number', placeholder: '0' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'risk_identification_process', label: 'Formal Risk Identification Process?', type: 'select', options: ['true', 'false'] },
        { id: 'third_party_risk_assessed', label: 'Third-Party Risks Assessed?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: null, fields: [
        { id: 'risk_ops_notes', label: 'Risk Operations Notes', type: 'textarea', placeholder: 'KRI breaches, emerging risks, appetite exceptions...', rows: 3 },
      ]},
    ],
  },
  {
    id: 'incident_oversight',
    title: 'Incident Oversight',
    tag: 'INCIDENT',
    tagClass: 'tag-grc',
    iconClass: 'cat-grc',
    icon: 'alert-triangle',
    desc: 'Incident log, root cause analysis, remediation tracking, regulator notification and lessons learned.',
    regs: 'FCA SYSC - ISO 22301 - DORA - NIST CSF',
    fields: [
      { row: 'cols-2', fields: [
        { id: 'firm_name', label: 'Firm Name', type: 'text', required: true },
        { id: 'frn', label: 'Body Ref', type: 'text' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'assessment_period', label: 'Assessment Period', type: 'text', placeholder: 'e.g. Q3 2026' },
        { id: 'total_incidents_period', label: 'Total Incidents in Period', type: 'number', placeholder: '0' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'critical_incidents', label: 'Critical Incidents', type: 'number', placeholder: '0' },
        { id: 'fca_notified', label: 'Regulator Notified?', type: 'select', options: ['false', 'true', 'N/A'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'fca_notification_datetime', label: 'Regulator Notification Date', type: 'date' },
        { id: 'fca_notification_reference', label: 'Regulator Notification Reference', type: 'text' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'root_cause_analysis_completed', label: 'Root Cause Analysis Done?', type: 'select', options: ['true', 'false'] },
        { id: 'remediation_on_track', label: 'Remediation On Track?', type: 'select', options: ['true', 'false', 'N/A'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'lessons_learned_documented', label: 'Lessons Learned Documented?', type: 'select', options: ['true', 'false'] },
        { id: 'incident_management_policy', label: 'Incident Management Policy Exists?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: null, fields: [
        { id: 'incident_notes', label: 'Incident Summary', type: 'textarea', placeholder: 'Key incidents, root causes, outstanding actions...', rows: 3 },
      ]},
    ],
  },
  {
    id: 'identity_data_risk',
    title: 'Identity, Data & Third-Party Risk',
    tag: 'IDR',
    tagClass: 'tag-grc',
    iconClass: 'cat-grc',
    icon: 'lock',
    desc: 'Identity governance, data classification, third-party risk assessments, access reviews and supply chain risk.',
    regs: 'GDPR - ISO 27001 - FCA PS26/2 - NIST CSF',
    fields: [
      { row: 'cols-2', fields: [
        { id: 'firm_name', label: 'Firm Name', type: 'text', required: true },
        { id: 'frn', label: 'Body Ref', type: 'text' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'assessment_period', label: 'Assessment Period', type: 'text', placeholder: 'e.g. Q3 2026' },
        { id: 'data_classification_policy', label: 'Data Classification Policy?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'access_reviews_completed', label: 'Access Reviews Completed (Qtrly)?', type: 'select', options: ['true', 'false'] },
        { id: 'privileged_access_mfa', label: 'Privileged Access MFA Enforced?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'third_party_risk_assessed', label: 'Critical Third-Party Risks Assessed?', type: 'select', options: ['true', 'false'] },
        { id: 'vendor_contracts_data_protection', label: 'Data Protection Clauses in Contracts?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'data_breach_response_plan', label: 'Data Breach Response Plan?', type: 'select', options: ['true', 'false'] },
        { id: 'gdpr_dpo_appointed', label: 'DPO / Privacy Officer Appointed?', type: 'select', options: ['true', 'false', 'N/A'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'supply_chain_risk_mapped', label: 'Supply Chain Risk Mapped?', type: 'select', options: ['true', 'false'] },
        { id: 'fourth_party_risk_considered', label: 'Fourth-Party Risk Considered?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: null, fields: [
        { id: 'idr_notes', label: 'Identity, Data & Risk Notes', type: 'textarea', placeholder: 'Access review findings, vendor risk issues, data incidents...', rows: 3 },
      ]},
    ],
  },
  // ── Threat & Security Reports (all regions) ───────────────────────────────
  {
    id: 'threat_intelligence',
    title: 'Threat Intelligence -- Banking',
    tag: 'INTEL',
    tagClass: 'tag-intel',
    iconClass: 'cat-intel',
    icon: 'target',
    desc: 'Sector threat landscape: fraud typologies, insider risk, sanctions evasion, emerging attack vectors.',
    regs: 'FCA SYSC - OFSI - SM&CR',
    fields: [
      { row: 'cols-2', fields: [
        { id: 'firm_name', label: 'Firm Name', type: 'text', required: true },
        { id: 'frn', label: 'FCA FRN', type: 'text' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'business_lines', label: 'Business Lines', type: 'text', placeholder: 'Retail Banking, Wealth Management, Custody...' },
        { id: 'geographic_footprint', label: 'Geographic Footprint', type: 'text', placeholder: 'UK, EU, APAC, Middle East...' },
      ]},
      { row: null, fields: [
        { id: 'assessment_period', label: 'Assessment Period', type: 'text', placeholder: 'e.g. Q3 2026' },
      ]},
    ],
  },
  {
    id: 'cyber_threat_assessment',
    title: 'Cyber Threat Assessment',
    tag: 'CBEST',
    tagClass: 'tag-cyber',
    iconClass: 'cat-cyber',
    icon: 'shield',
    desc: 'FCA CBEST, PS21/3 operational resilience. Pen test status, MFA, endpoint protection scoring.',
    regs: 'FCA PS21/3 - CBEST - SYSC',
    fields: [
      { row: 'cols-2', fields: [
        { id: 'firm_name', label: 'Firm Name', type: 'text', required: true },
        { id: 'frn', label: 'FCA FRN', type: 'text' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'cbest_assessment_completed', label: 'CBEST Assessment Completed?', type: 'select', options: ['true', 'false'] },
        { id: 'last_cbest_date', label: 'Last CBEST Date', type: 'date' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'ibs_identified', label: 'Important Business Services Identified?', type: 'select', options: ['true', 'false'] },
        { id: 'impact_tolerances_set', label: 'Impact Tolerances Set?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'scenario_testing_completed', label: 'Scenario Testing Completed?', type: 'select', options: ['true', 'false'] },
        { id: 'mfa_on_critical_systems', label: 'MFA on Critical Systems?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'privileged_access_management', label: 'Privileged Access Management?', type: 'select', options: ['true', 'false'] },
        { id: 'cyber_incident_response_plan_exists', label: 'Cyber IR Plan Exists?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'cyber_response_plan_tested', label: 'Cyber IR Plan Tested?', type: 'select', options: ['true', 'false'] },
        { id: 'third_party_cyber_risk_assessed', label: 'Third-Party Cyber Risk Assessed?', type: 'select', options: ['true', 'false'] },
      ]},
    ],
  },
  {
    id: 'fca_incident_response',
    title: 'FCA Incident Response',
    tag: 'FCA 24HR',
    tagClass: 'tag-fca',
    iconClass: 'cat-fca',
    icon: 'bell',
    desc: 'FCA 24-hour operational incident reporting (PS26/2), CASS breach procedures, remediation.',
    regs: 'PS26/2 - FCA SUP - CASS - UK GDPR',
    fields: [
      { row: 'cols-2', fields: [
        { id: 'firm_name', label: 'Firm Name', type: 'text', required: true },
        { id: 'frn', label: 'FCA FRN', type: 'text' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'incident_type', label: 'Incident Type', type: 'select', options: ['CASS Breach', 'Cyber Incident', 'Data Breach', 'Operational Failure', 'Fraud', 'Other'] },
        { id: 'incident_datetime', label: 'Incident Date & Time', type: 'datetime-local', required: true },
      ]},
      { row: 'cols-2', fields: [
        { id: 'fca_notified', label: 'FCA Notified?', type: 'select', options: ['false', 'true'] },
        { id: 'fca_notification_datetime', label: 'FCA Notification Date & Time', type: 'datetime-local' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'fca_notification_reference', label: 'FCA Notification Reference', type: 'text', placeholder: 'Reference number if available' },
        { id: 'ico_notified', label: 'ICO Notified?', type: 'select', options: ['false', 'true'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'incident_contained', label: 'Incident Contained?', type: 'select', options: ['false', 'true'] },
        { id: 'containment_date', label: 'Containment Date', type: 'date' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'clients_affected', label: 'Clients Affected', type: 'number', placeholder: '0' },
        { id: 'client_assets_affected', label: 'Client Assets Affected?', type: 'select', options: ['false', 'true'] },
      ]},
      { row: null, fields: [
        { id: 'client_assets_amount', label: 'Client Assets Amount (if affected)', type: 'text', placeholder: 'e.g. GBP 2.5m' },
      ]},
      { row: null, fields: [
        { id: 'root_cause', label: 'Root Cause', type: 'textarea', placeholder: 'Identified or suspected root cause...', rows: 2 },
      ]},
      { row: null, fields: [
        { id: 'timeline', label: 'Incident Timeline', type: 'textarea', placeholder: 'Chronology of key events...', rows: 2 },
      ]},
      { row: null, fields: [
        { id: 'lessons_learned', label: 'Lessons Learned', type: 'textarea', placeholder: 'What has the firm learned from this incident?', rows: 2 },
      ]},
      { row: null, fields: [
        { id: 'remediation_actions', label: 'Remediation Actions', type: 'textarea', placeholder: 'Steps being taken to contain and remediate...', rows: 2 },
      ]},
    ],
  },
  {
    id: 'due_diligence',
    title: 'Due Diligence',
    tag: 'DD',
    tagClass: 'tag-fca',
    iconClass: 'cat-fca',
    icon: 'search',
    desc: 'FCA Fit & Proper assessment, third-party CASS 6 & 7 compliance, PEP/sanctions screening.',
    regs: 'FCA FIT - CASS 6 - CASS 7 - OFSI',
    fields: [
      { row: 'cols-2', fields: [
        { id: 'subject_name', label: 'Subject Name', type: 'text', required: true, placeholder: 'Entity or individual' },
        { id: 'subject_type', label: 'Subject Type', type: 'select', options: ['Third-Party Custodian', 'Counterparty', 'Senior Manager', 'Supplier', 'JV Partner'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'purpose', label: 'Purpose of Review', type: 'text', placeholder: 'e.g. New supplier onboarding, SMF appointment...' },
        { id: 'fca_frn_or_irn', label: 'FCA FRN', type: 'text', placeholder: 'FRN or IRN if applicable' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'fca_registration_required', label: 'FCA Registration Required?', type: 'select', options: ['true', 'false'] },
        { id: 'fca_registered', label: 'FCA Registered?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'supplier_fca_authorised', label: 'Supplier FCA Authorised?', type: 'select', options: ['true', 'false'] },
        { id: 'written_agreement_in_place', label: 'Written Agreement in Place?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'sanctions_match', label: 'Sanctions Match Found?', type: 'select', options: ['false', 'true'] },
        { id: 'criminal_convictions', label: 'Criminal Convictions?', type: 'select', options: ['false', 'true'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'ccjs_or_bankruptcy', label: 'CCJs or Bankruptcy?', type: 'select', options: ['false', 'true'] },
        { id: 'prior_regulatory_actions', label: 'Prior Regulatory Actions?', type: 'select', options: ['false', 'true'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'active_fca_ban_or_prohibition', label: 'Active FCA Ban / Prohibition?', type: 'select', options: ['false', 'true'] },
        { id: 'professional_qualifications_verified', label: 'Qualifications Verified?', type: 'select', options: ['true', 'false'] },
      ]},
    ],
  },
  {
    id: 'country_risk',
    title: 'Country Risk',
    tag: 'SANCTIONS',
    tagClass: 'tag-risk',
    iconClass: 'cat-risk',
    icon: 'globe',
    desc: 'Cross-border client asset risk, sanctions regimes (OFSI/OFAC), AML risk rating, local custody.',
    regs: 'OFSI - OFAC - FATF - CASS',
    fields: [
      { row: 'cols-2', fields: [
        { id: 'country', label: 'Country', type: 'text', required: true, placeholder: 'Russia, UAE, Cayman Islands...' },
        { id: 'purpose', label: 'Purpose of Assessment', type: 'text', placeholder: 'e.g. Client onboarding, investment, correspondent banking' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'sanctions_applicable', label: 'Sanctions Applicable?', type: 'select', options: ['false', 'true'] },
        { id: 'fatf_grey_list', label: 'FATF Grey / Black List?', type: 'select', options: ['false', 'true'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'corruption_perceptions_index_score', label: 'CPI Score (0-100)', type: 'number', placeholder: '50' },
        { id: 'political_stability', label: 'Political Stability', type: 'select', options: ['Stable', 'Moderate', 'Unstable', 'Failed State'] },
      ]},
      { row: null, fields: [
        { id: 'fca_prior_concern', label: 'FCA Prior Concern about this Country?', type: 'select', options: ['false', 'true'] },
      ]},
    ],
  },
  {
    id: 'executive_protection',
    title: 'Executive Protection (SM&CR)',
    tag: 'SM&CR',
    tagClass: 'tag-exec',
    iconClass: 'cat-exec',
    icon: 'user',
    desc: 'Senior Manager risk briefings, SM&CR mapping, prescribed responsibilities, certification regime.',
    regs: 'SM&CR - FCA FIT - COCON',
    fields: [
      { row: 'cols-2', fields: [
        { id: 'subject_name', label: 'Subject Name', type: 'text', required: true, placeholder: 'Full name of Senior Manager' },
        { id: 'subject_role', label: 'Subject Role', type: 'text', placeholder: 'CEO, CFO, CRO, SMF holder...' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'firm_name', label: 'Firm Name', type: 'text' },
        { id: 'frn', label: 'FCA FRN', type: 'text' },
      ]},
      { row: null, fields: [
        { id: 'smf_functions', label: 'SMF Functions Held', type: 'text', placeholder: 'e.g. SMF1 (CEO), SMF4 (Chief Risk), SMF16 (Compliance)...' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'public_profile_level', label: 'Public Profile Level', type: 'select', options: ['High', 'Medium', 'Low'] },
        { id: 'international_travel_frequency', label: 'International Travel Frequency', type: 'select', options: ['Frequent', 'Occasional', 'Rare', 'Never'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'travel_destinations', label: 'Travel Destinations', type: 'text', placeholder: 'Countries or regions visited...' },
        { id: 'home_working', label: 'Home Working?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'known_threats_or_incidents', label: 'Known Threats or Incidents?', type: 'select', options: ['false', 'true'] },
        { id: 'harassment_or_protest_targeting', label: 'Harassment / Protest Targeting?', type: 'select', options: ['false', 'true'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'digital_footprint_concerns', label: 'Digital Footprint Concerns?', type: 'select', options: ['false', 'true'] },
      ]},
      { row: null, fields: [
        { id: 'protective_measures_in_place', label: 'Protective Measures in Place', type: 'textarea', placeholder: 'Describe existing security arrangements...', rows: 2 },
      ]},
    ],
  },
  {
    id: 'physical_security_audit',
    title: 'Physical Security Audit',
    tag: 'PHYSICAL',
    tagClass: 'tag-phys',
    iconClass: 'cat-phys',
    icon: 'building',
    desc: 'Branch / office / data centre -- access control, CCTV, alarms, FCA operational resilience.',
    regs: 'FCA PS21/3 - NPSA - CPNI',
    fields: [
      { row: 'cols-2', fields: [
        { id: 'firm_name', label: 'Firm Name', type: 'text', required: true },
        { id: 'frn', label: 'FCA FRN', type: 'text' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'premises_type', label: 'Premises Type', type: 'select', options: ['Branch', 'Head Office', 'Data Centre', 'Vault', 'Disaster Recovery Site'] },
        { id: 'address', label: 'Address', type: 'text', placeholder: 'Full premises address' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'access_control_in_place', label: 'Access Control?', type: 'select', options: ['true', 'false'] },
        { id: 'access_control_type', label: 'Access Control Type', type: 'text', placeholder: 'Fob, Biometric, PIN...' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'cctv_coverage', label: 'CCTV Coverage?', type: 'select', options: ['true', 'false'] },
        { id: 'cctv_areas_covered', label: 'CCTV Areas', type: 'text', placeholder: 'Reception, Server Room...' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'intruder_alarm', label: 'Intruder Alarm?', type: 'select', options: ['true', 'false'] },
        { id: 'alarm_standard', label: 'Alarm Standard', type: 'text', placeholder: 'PD 6662, BS 8243...' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'security_personnel_on_site', label: 'Security Personnel?', type: 'select', options: ['true', 'false'] },
        { id: 'security_hours', label: 'Security Hours', type: 'text', placeholder: '24/7, 09:00-18:00...' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'perimeter_security', label: 'Perimeter Security?', type: 'select', options: ['true', 'false'] },
        { id: 'visitor_management_process', label: 'Visitor Management?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'secure_document_disposal', label: 'Secure Doc Disposal?', type: 'select', options: ['true', 'false'] },
        { id: 'business_continuity_plan_for_premises', label: 'BCP for Premises?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'last_physical_security_review_date', label: 'Last Security Review', type: 'date' },
        { id: 'prior_incidents', label: 'Prior Incidents', type: 'text', placeholder: 'Leave blank if none' },
      ]},
      { row: null, fields: [
        { id: 'prior_incidents_remediated', label: 'Prior Incidents Remediated?', type: 'select', options: ['true', 'false'] },
      ]},
    ],
  },
  {
    id: 'grc_report',
    title: 'GRC Intelligence Report',
    tag: 'GRC',
    tagClass: 'tag-grc',
    iconClass: 'cat-grc',
    icon: 'target',
    desc: 'Governance, Risk & Compliance maturity assessment — OCEG/COSO methodology, FCA expectations, SMCR alignment.',
    regs: 'FCA PS26/2 - SM&CR - OCEG - ISO 31000',
    fields: [
      { row: 'cols-2', fields: [
        { id: 'firm_name', label: 'Firm Name', type: 'text', placeholder: 'e.g. Meridian Capital Partners Ltd', required: true },
        { id: 'frn', label: 'FCA FRN', type: 'text', placeholder: '123456' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'assessment_period', label: 'Assessment Period', type: 'text', placeholder: 'e.g. Q3 2026' },
        { id: 'grc_platform_in_use', label: 'GRC Platform in Use?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'governance_board_oversight', label: 'Board Oversight of GRC?', type: 'select', options: ['true', 'false'] },
        { id: 'governance_policy_doc_current', label: 'Policy Documents Current?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'governance_policy_comprehension_rate', label: 'Policy Comprehension Rate (%)', type: 'number', placeholder: '85' },
        { id: 'governance_decision_framework', label: 'Decision Framework Exists?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'risk_appetite_defined', label: 'Risk Appetite Defined?', type: 'select', options: ['true', 'false'] },
        { id: 'risk_register_maintained', label: 'Risk Register Maintained?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'risk_register_last_reviewed', label: 'Risk Register Last Reviewed', type: 'date' },
        { id: 'risk_open_items', label: 'Open Risk Items', type: 'number', placeholder: '12' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'risk_critical_items', label: 'Critical / HIGH Risk Items', type: 'number', placeholder: '2' },
        { id: 'risk_identification_process', label: 'Formal Risk ID Process?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'third_party_risk_assessed', label: 'Third-Party Risk Assessed?', type: 'select', options: ['true', 'false'] },
        { id: 'compliance_regulatory_monitoring', label: 'Regulatory Monitoring?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'compliance_training_completion_rate', label: 'Training Completion Rate (%)', type: 'number', placeholder: '90' },
        { id: 'compliance_control_effectiveness', label: 'Control Effectiveness (%)', type: 'number', placeholder: '78' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'compliance_audit_findings_open', label: 'Open Audit Findings', type: 'number', placeholder: '3' },
        { id: 'fca_regulatory_changes_tracked', label: 'FCA Changes Tracked?', type: 'select', options: ['true', 'false'] },
      ]},
    ],
  },
  {
    id: 'blacklist_report',
    title: 'FATF Blacklist Intelligence Report',
    tag: 'AML/CFT',
    tagClass: 'tag-risk',
    iconClass: 'cat-risk',
    icon: 'alert',
    desc: 'FATF jurisdictional risk, EDD obligations, AML/CFT controls, SAR assessment and correspondent banking screening under UK MLR 2017.',
    regs: 'FATF 40 Recs - UK MLR 2017 - POCA 2002 - OFSI - FCA FCG',
    fields: [
      { row: 'cols-2', fields: [
        { id: 'firm_name', label: 'Firm Name', type: 'text', placeholder: 'e.g. Meridian Capital Partners Ltd', required: true },
        { id: 'frn', label: 'FCA FRN', type: 'text', placeholder: '123456' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'counterparty_name', label: 'Counterparty / Subject Name', type: 'text', placeholder: 'e.g. XYZ Bank Ltd', required: true },
        { id: 'counterparty_type', label: 'Counterparty Type', type: 'select', options: ['Direct Client', 'Correspondent Bank', 'Trade Finance', 'Investment', 'Payment Processing'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'client_category', label: 'Client Category', type: 'select', options: ['Institutional', 'Retail', 'PEP', 'Charity / NPO', 'High Net Worth', 'Shell / Holding Company'] },
        { id: 'transaction_type', label: 'Transaction Type', type: 'text', placeholder: 'e.g. Trade Finance — Letter of Credit' },
      ]},
      { row: null, fields: [
        { id: 'countries_involved', label: 'Countries Involved (comma-separated)', type: 'text', placeholder: 'e.g. Nigeria, Dubai, UK', required: true },
      ]},
      { row: 'cols-2', fields: [
        { id: 'assessment_period', label: 'Assessment Period', type: 'text', placeholder: 'e.g. Q4 2026' },
        { id: 'edd_procedures_in_place', label: 'EDD Procedures in Place?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'sanctions_screening_performed', label: 'Sanctions Screening Performed?', type: 'select', options: ['true', 'false'] },
        { id: 'sanctions_screening_tool', label: 'Screening Tool Used', type: 'text', placeholder: 'e.g. WorldCheck, ComplyAdvantage' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'pep_screening_performed', label: 'PEP Screening Performed?', type: 'select', options: ['true', 'false'] },
        { id: 'adverse_media_screening', label: 'Adverse Media Screening?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'source_of_funds_verified', label: 'Source of Funds Verified?', type: 'select', options: ['true', 'false'] },
        { id: 'beneficial_owner_identified', label: 'Beneficial Owner (UBO) Identified?', type: 'select', options: ['true', 'false'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'sar_filing_required', label: 'SAR Filing Required?', type: 'select', options: ['false', 'true'] },
        { id: 'sar_filed', label: 'SAR Filed with NCA?', type: 'select', options: ['false', 'true'] },
      ]},
      { row: 'cols-2', fields: [
        { id: 'aml_training_completion_rate', label: 'AML Training Completion Rate (%)', type: 'number', placeholder: '92' },
        { id: 'last_aml_risk_assessment_date', label: 'Last Firm-Wide AML Risk Assessment', type: 'date' },
      ]},
      { row: 'cols-2', fields: [
        { id: 'correspondent_bank_relationships', label: 'Correspondent Bank Relationships?', type: 'select', options: ['false', 'true'] },
        { id: 'correspondent_bank_in_listed_jurisdiction', label: 'Corr. Bank in FATF-Listed Jurisdiction?', type: 'select', options: ['false', 'true'] },
      ]},
      { row: null, fields: [
        { id: 'shell_bank_check_performed', label: 'Shell Bank Check Performed?', type: 'select', options: ['true', 'false'] },
      ]},
    ],
  },
  {
    id: 'grc_templates',
    title: 'GRC Templates & Platform Guide',
    tag: 'RESOURCE',
    tagClass: 'tag-grc',
    iconClass: 'cat-grc',
    icon: 'clipboard',
    desc: 'GRC toolkit',
    regs: 'ISO 27001 - DORA - GDPR - SOC 2 - NIST',
    href: '/grc-templates',
    fields: [],
  },
];

// -- Region selector ---------------------------------------------------------
const REGIONS = [
  { slug: 'uk',            flag: '🌍', short: '🌍 UK',          label: 'United Kingdom',  regs: 'FCA · CASS · SM&CR · Bank of England · PRA' },
  { slug: 'north-america', flag: '🌎',  short: '🌎 N. America',    label: 'North America',   regs: 'Fed · SEC · OCC · FinCEN · OFAC · OSFI · FINTRAC' },
  { slug: 'latin-america', flag: '🌎',  short: '🌎 L. America',    label: 'Latin America',   regs: 'BCB · CVM · BANXICO · CNBV · SFC · CMF · GAFILAT' },
  { slug: 'asia-pacific',  flag: '🌏',  short: '🌏 Asia Pacific',  label: 'Asia-Pacific',    regs: 'MAS · HKMA · FSA · RBI · SEBI · ASIC · APRA' },
  { slug: 'africa',        flag: '🌍',  short: '🌍 Africa',        label: 'Africa',          regs: 'FSCA · CBN · CBK · CMA · GIABA · ESAAMLG' },
  { slug: 'europe',        flag: '🌍', short: '🌍 Europe',       label: 'Europe',          regs: 'ESMA · ECB · EBA · AMLA · BaFin · AMF · DORA' },
];

let selectedRegion = 'uk';

function _regionCfg() { return REGIONS.find(r => r.slug === selectedRegion) || REGIONS[0]; }

// Regional card-title overrides for the 4 CASS report suite reports
const _CASS_TITLES = {
  cass_health_check:    { uk:'CASS Health Check', 'north-america':'SEC / BSA-AML Client Assets Health Check', 'latin-america':'BCB / CVM Client Funds Health Check', 'asia-pacific':'MAS / ASIC / HKMA Client Protection Check', europe:'MiCA / DORA Client Assets Health Check', africa:'FSCA / CBN / CBK Client Funds Health Check' },
  cass_resolution_pack: { uk:'CASS Resolution Pack Readiness', 'north-america':'SEC / SIPC Asset Return Readiness', 'latin-america':'BCB / CVM Resolution Readiness', 'asia-pacific':'MAS / ASIC Asset Resolution Readiness', europe:'DORA / MiFID II Recovery Plan Readiness', africa:'FSCA / CBN Recovery Plan Readiness' },
  cass_breach_log:      { uk:'CASS Breach Log & Remediation', 'north-america':'SEC / FINRA Violation Log', 'latin-america':'BCB / CVM Breach Log', 'asia-pacific':'MAS / ASIC / SEBI Breach Register', europe:'DORA / MiCA Incident Register', africa:'FSCA / CBN / CBK Violation Register' },
  cass_oversight:       { uk:'CASS Oversight (COOF)', 'north-america':'CCO / BSA Compliance Oversight Report', 'latin-america':'BCB / CVM Governance & Oversight', 'asia-pacific':'MAS / ASIC Board Compliance Oversight', europe:'ESMA / AMLA Governance Oversight', africa:'FSCA / CBN Board Compliance Report' },
};
const _CASS_TAGS = {
  cass_health_check:    { uk:'CASS 6 & 7', 'north-america':'SEC / CFTC', 'latin-america':'BCB / CVM', 'asia-pacific':'MAS / ASIC', europe:'MiCA / DORA', africa:'FSCA / CBN' },
  cass_resolution_pack: { uk:'CASS 10', 'north-america':'SEC / SIPC', 'latin-america':'BCB / CVM', 'asia-pacific':'MAS / ASIC', europe:'DORA', africa:'FSCA / CBN' },
  cass_breach_log:      { uk:'CASS BREACH', 'north-america':'SEC / FINRA', 'latin-america':'BCB / CVM', 'asia-pacific':'MAS / ASIC', europe:'DORA / MiCA', africa:'FSCA / CBN' },
  cass_oversight:       { uk:'COOF', 'north-america':'CCO / BSA', 'latin-america':'BCB / CVM', 'asia-pacific':'MAS / ASIC', europe:'ESMA / AMLA', africa:'FSCA / CBN' },
};
const _FIELD_LABELS_NONUK = {
  cass_category:                       'Regulatory Category',
  alternative_method_fca_agreed:       'Regulator-Approved Method?',
  coof_individual_named:               'Compliance Officer Named?',
  coof_individual_name:                'Compliance Officer Name',
  coof_last_review_date:               'Compliance Review Date',
  cass_breaches_last_12_months:        'Regulatory Breaches in Last 12 Months?',
  retail_interest_paid:                'Client Interest Paid?',
  custodian_selection_grounds_recorded:'Custodian Selection Grounds Recorded?',
  is_payment_or_emoney_firm:           'Payment / E-Money Firm?',
  last_coof_review_of_cass_date:       'Last Compliance Review Date',
  last_coof_report_to_board_date:      'Last Oversight Report to Board',
  board_minutes_confirm_coof_report:   'Board Minutes Confirm Oversight Report?',
  outstanding_coof_recommendations:    'Outstanding Compliance Recommendations',
  fca_notified:                        'Regulator Notified?',
  fca_notification_datetime:           'Regulator Notification Date & Time',
  fca_notification_reference:          'Regulator Notification Reference',
};

function _injectRSStyles() {
  if (document.getElementById('rs-style')) return;
  const s = document.createElement('style'); s.id = 'rs-style';
  s.textContent = `
    .rs-bar{display:flex;align-items:center;gap:10px;padding:12px 0 10px;flex-wrap:wrap;margin-bottom:4px}
    .rs-label{font-size:.65rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--text-3);font-family:'IBM Plex Mono',monospace;white-space:nowrap;flex-shrink:0}
    .rs-pills{display:flex;flex-wrap:wrap;gap:6px;flex:1}
    .rs-pill{display:inline-flex;align-items:center;gap:4px;padding:5px 11px;border-radius:20px;border:1px solid var(--border-dim);background:var(--surface-1);color:var(--text-2);font-size:.70rem;font-weight:600;cursor:pointer;transition:all .14s;font-family:'IBM Plex Mono',monospace;white-space:nowrap}
    .rs-pill:hover{border-color:var(--accent);color:var(--accent)}
    .rs-pill.rs-active{background:var(--accent);border-color:var(--accent);color:#fff}
    .rs-ctx{font-size:.63rem;color:var(--text-3);font-family:'IBM Plex Mono',monospace;letter-spacing:.01em;width:100%;padding:0 2px;margin-top:-2px}
    @media(max-width:620px){.rs-ctx{display:none}}
  `;
  document.head.appendChild(s);
}

function _twemoji(el) {
  if (typeof twemoji !== 'undefined' && el) twemoji.parse(el, { folder: 'svg', ext: '.svg' });
}

function renderRegionSelector() {
  _injectRSStyles();
  const grid = document.getElementById('reports-grid');
  if (!grid) return;
  document.getElementById('rs-bar')?.remove();
  const bar = document.createElement('div'); bar.id = 'rs-bar'; bar.className = 'rs-bar';
  bar.innerHTML = `
    <span class="rs-label" id="rs-label"><span id="rs-flag">${_regionCfg().flag}</span> Report Suite</span>
    <div class="rs-pills">
      ${REGIONS.map(r => `<button class="rs-pill${r.slug === selectedRegion ? ' rs-active' : ''}" data-slug="${r.slug}" title="${r.label} — ${r.regs}">${r.short}</button>`).join('')}
    </div>
    <span class="rs-ctx" id="rs-ctx">${_regionCfg().regs}</span>`;
  // Insert ABOVE the section-header (before the "Report Suite" title), not just before the grid
  const sectionHeader = grid.parentNode.querySelector('.section-header');
  if (sectionHeader) {
    grid.parentNode.insertBefore(bar, sectionHeader);
  } else {
    grid.parentNode.insertBefore(bar, grid);
  }
  bar.querySelectorAll('.rs-pill').forEach(btn => btn.addEventListener('click', () => {
    selectedRegion = btn.dataset.slug;
    bar.querySelectorAll('.rs-pill').forEach(b => b.classList.remove('rs-active'));
    btn.classList.add('rs-active');
    const _rc = _regionCfg();
    document.getElementById('rs-ctx').textContent = _rc.regs;
    document.getElementById('rs-flag').textContent = _rc.flag;
    history.replaceState(null, '', `?region=${selectedRegion}`);
    // Update section title and re-render cards with regional labels
    const sTitle = document.querySelector('.section-header .section-title');
    const rc = _regionCfg();
    if (sTitle) sTitle.textContent = rc.slug === 'uk' ? 'Report Suite' : `Report Suite — ${rc.short}`;
    renderCards();
    updateFilterBadges();
    _twemoji(document.getElementById('rs-flag'));
  }));
  _twemoji(bar);
}

function initFromURL() {
  const p = new URLSearchParams(window.location.search);
  const r = p.get('region');
  const rep = p.get('report');
  if (r && REGIONS.find(x => x.slug === r)) selectedRegion = r;
  if (rep) requestAnimationFrame(() => openModal(rep));
}

// -- State -------------------------------------------------------------------
let activeReport = null;
let currentEventSource = null;

// -- Particles ---------------------------------------------------------------
function initParticles() {
  const canvas = document.getElementById('particle-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let W = window.innerWidth, H = window.innerHeight;
  canvas.width = W; canvas.height = H;
  window.addEventListener('resize', () => {
    W = canvas.width = window.innerWidth;
    H = canvas.height = window.innerHeight;
  });
  const particles = Array.from({ length: 40 }, () => ({
    x: Math.random() * W, y: Math.random() * H,
    vx: (Math.random() - 0.5) * 0.25, vy: (Math.random() - 0.5) * 0.25,
    r: Math.random() * 1.0 + 0.3,
    a: Math.random() * 0.25 + 0.04,
  }));
  function draw() {
    ctx.clearRect(0, 0, W, H);
    particles.forEach(p => {
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0) p.x = W; if (p.x > W) p.x = 0;
      if (p.y < 0) p.y = H; if (p.y > H) p.y = 0;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(62, 189, 250, ${p.a})`;
      ctx.fill();
    });
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const d = Math.sqrt(dx * dx + dy * dy);
        if (d < 110) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(62, 130, 250, ${0.06 * (1 - d / 110)})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(draw);
  }
  draw();
}

// -- Clock -------------------------------------------------------------------
function initClock() {
  const el = document.getElementById('time-display');
  if (!el) return;
  function tick() {
    el.textContent = new Date().toLocaleString('en-GB', {
      timeZone: 'UTC',
      day: '2-digit', month: 'short', year: 'numeric',
      hour: '2-digit', minute: '2-digit', second: '2-digit',
    }) + ' UTC';
  }
  tick();
  setInterval(tick, 1000);
}

// -- AI Status ---------------------------------------------------------------
const AI_PROVIDER_META = {
  OpenRouter:  { label: 'OpenRouter', badge: 'FREE', cls: 'badge-free', tip: '29+ free models, auto-routed' },
  Cerebras:    { label: 'Cerebras',   badge: '14K',  cls: 'badge-fast', tip: 'Fastest free inference — 14,400 RPD' },
  Groq:        { label: 'Groq',       badge: '1K',   cls: 'badge-fast', tip: 'Fast inference — 1,000 RPD free' },
  Mistral:     { label: 'Mistral',    badge: 'EU',   cls: 'badge-eu',   tip: 'EU-hosted (France) — 1B tokens/month free' },
  LLM7:        { label: 'LLM7.io',   badge: 'UK',   cls: 'badge-uk',   tip: 'UK-hosted — optimised for FCA workloads' },
  GitHub:      { label: 'GitHub',     badge: 'PAT',  cls: 'badge-free', tip: 'GitHub Models — GPT-4o, Llama 3.3 70B' },
  Cohere:      { label: 'Cohere',     badge: 'CMD',  cls: 'badge-free', tip: 'Command-A — 1,000 req/month free' },
  Gemini:      { label: 'Gemini',     badge: '1.5K', cls: 'badge-free', tip: 'Gemini Flash — 1,500 RPD' },
  Anthropic:   { label: 'Anthropic',  badge: 'HAI',  cls: 'badge-free', tip: 'Claude Haiku 4.5 — 50 RPM' },
  DeepSeek:    { label: 'DeepSeek',   badge: 'V3',   cls: 'badge-fast', tip: 'DeepSeek V3 — strong reasoning, 60 RPM' },
  OpenAI:      { label: 'OpenAI',     badge: 'PAID', cls: 'badge-paid', tip: 'Paid OpenAI key configured' },
};

async function loadAIStatus() {
  try {
    const res = await fetch('/api/status');
    const data = await res.json();
    const connectors = data.ai_connectors || {};
    const chain = data.ai_fallback_chain || [];
    const bar = document.getElementById('ai-chips');
    if (!bar) return;
    bar.innerHTML = '';

    const allNames = [...new Set([...chain, ...Object.keys(AI_PROVIDER_META)])];
    let onlineCount = 0;
    allNames.forEach(key => {
      const cKey = key.charAt(0).toUpperCase() + key.slice(1);
      const online = connectors[key] || connectors[cKey] || connectors[key.toLowerCase()];
      const meta = AI_PROVIDER_META[cKey] || AI_PROVIDER_META[key] || { label: key, badge: '', cls: '', tip: key };
      if (online) onlineCount++;
      const chip = document.createElement('div');
      chip.className = `ai-chip ${online ? 'online' : 'offline'}`;
      chip.title = meta.tip + (online ? ' — configured' : ' — add key to .env');
      chip.innerHTML = `<span class="dot"></span>${meta.label}${meta.badge ? `<span class="ai-badge ${meta.cls}">${meta.badge}</span>` : ''}`;
      bar.appendChild(chip);
    });

    const stat = document.getElementById('stat-reports');
    if (stat) animateStat(stat, data.reports_generated ?? 0);

    const aiStat = document.getElementById('stat-ai-connectors');
    if (aiStat) animateStat(aiStat, onlineCount);

    if (data.uk_hosted_available) {
      showToast('UK-hosted AI (LLM7.io) active — optimised for FCA workloads', 'success');
    } else if (onlineCount > 0) {
      showToast(`${onlineCount} AI provider${onlineCount > 1 ? 's' : ''} active in fallback chain`, 'info');
    }
  } catch (e) {
    console.warn('Status fetch failed', e);
  }
}

// -- Category filter ---------------------------------------------------------
let activeFilter = 'all';

function initFilter() {
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      activeFilter = btn.dataset.cat;
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      applyFilter();
    });
  });
}

function applyFilter() {
  document.querySelectorAll('.report-card').forEach(card => {
    if (activeFilter === 'all' || card.dataset.cat === activeFilter) {
      card.classList.remove('hidden');
    } else {
      card.classList.add('hidden');
    }
  });
}

// -- Filter badge counts -----------------------------------------------------
function updateFilterBadges() {
  const counts = {};
  REPORTS.forEach(r => {
    const cat = r.iconClass.replace('cat-', '');
    counts[cat] = (counts[cat] || 0) + 1;
  });
  document.querySelectorAll('.filter-btn').forEach(btn => {
    const cat = btn.dataset.cat;
    const n = cat === 'all' ? REPORTS.length : (counts[cat] || 0);
    if (!btn.querySelector('.f-badge')) {
      const b = document.createElement('span');
      b.className = 'f-badge';
      btn.appendChild(b);
    }
    btn.querySelector('.f-badge').textContent = n;
  });
}

// -- Render cards ------------------------------------------------------------
function renderCards() {
  const grid = document.getElementById('reports-grid');
  if (!grid) return;
  grid.innerHTML = '';

  REPORTS.forEach((r, i) => {
    const cat = r.iconClass.replace('cat-', '');
    const card = document.createElement('div');
    card.className = 'report-card';
    card.dataset.cat = cat;
    const cardTitle = (_CASS_TITLES[r.id] && _CASS_TITLES[r.id][selectedRegion]) || r.title;
    const cardTag   = (_CASS_TAGS[r.id]   && _CASS_TAGS[r.id][selectedRegion])   || r.tag;
    card.innerHTML = `
      <div class="card-header">
        <div class="card-icon ${r.iconClass}">${ICONS[r.icon] || ''}</div>
        <div class="card-tag ${r.tagClass}">${cardTag}</div>
      </div>
      <div class="card-title">${cardTitle}</div>
      <div class="card-desc">${r.desc}</div>
      <div class="card-footer">
        <span class="card-regs">${r.regs}</span>
        <span class="card-arrow">${ICONS.arrow}</span>
      </div>`;
    card.addEventListener('click', () => r.href ? (window.location.href = r.href) : openModal(r.id));
    if (r.href) card.style.cursor = 'pointer';
    grid.appendChild(card);

    // Staggered entrance
    requestAnimationFrame(() => {
      setTimeout(() => card.classList.add('entered'), 60 + i * 38);
    });
  });
  _twemoji(grid);
}

// -- Modal -------------------------------------------------------------------
function openModal(reportId) {
  const report = REPORTS.find(r => r.id === reportId);
  if (!report) return;
  activeReport = report;

  const iconWrap = document.getElementById('modal-icon-wrap');
  if (iconWrap) iconWrap.innerHTML = ICONS[report.icon] || '';
  const _modalTitle = (_CASS_TITLES[report.id] && _CASS_TITLES[report.id][selectedRegion]) || report.title;
  const _modalTag   = (_CASS_TAGS[report.id]   && _CASS_TAGS[report.id][selectedRegion])   || report.tag;
  document.getElementById('modal-title').textContent = _modalTitle;
  document.getElementById('modal-sub').textContent = `${_modalTag} - ${report.regs}`;

  const form = document.getElementById('report-form');
  form.innerHTML = '';
  report.fields.forEach(rowDef => {
    const row = document.createElement('div');
    row.className = `form-row${rowDef.row ? ' ' + rowDef.row : ''}`;
    rowDef.fields.forEach(f => row.appendChild(buildField(f)));
    form.appendChild(row);
  });

  // Region banner
  const rc = _regionCfg();
  let banner = document.getElementById('modal-region-banner');
  if (!banner) {
    banner = document.createElement('div'); banner.id = 'modal-region-banner';
    banner.style.cssText = 'display:flex;align-items:center;gap:8px;padding:7px 14px;margin-bottom:14px;border-radius:8px;background:var(--surface-2);border:1px solid var(--border-dim);font-size:.70rem;font-family:"IBM Plex Mono",monospace;color:var(--text-2)';
    document.getElementById('report-form').parentNode.insertBefore(banner, document.getElementById('report-form'));
  }
  banner.innerHTML = `<span style="font-size:1rem">${rc.flag}</span><span style="font-weight:700;color:var(--text-1)">${rc.label}</span><span style="color:var(--text-3)">·</span><span>${rc.regs}</span>`;

  document.getElementById('scan-option').style.display = 'flex';
  resetProgress();
  document.getElementById('modal-backdrop').classList.add('open');
  setTimeout(() => form.querySelector('input, select, textarea')?.focus(), 180);
}

function buildField(f) {
  const g = document.createElement('div');
  g.className = 'form-group';
  const lbl = document.createElement('label');
  lbl.htmlFor = f.id;
  const _fieldLabel = (f.id === 'frn' || f.id === 'fca_frn_or_irn')
    ? (selectedRegion === 'uk' ? 'FCA FRN' : 'Bodie Ref:')
    : (selectedRegion !== 'uk' && _FIELD_LABELS_NONUK[f.id]) || f.label;
  lbl.textContent = _fieldLabel + (f.required ? ' *' : '');
  const tip = FIELD_TOOLTIPS[f.id];
  if (tip) {
    const icon = document.createElement('span');
    icon.className = 'field-tip';
    icon.setAttribute('aria-label', tip);
    icon.textContent = '?';
    icon.addEventListener('mouseenter', e => showFieldTip(e, tip));
    icon.addEventListener('mouseleave', hideFieldTip);
    icon.addEventListener('focus', e => showFieldTip(e, tip));
    icon.addEventListener('blur', hideFieldTip);
    lbl.appendChild(icon);
  }
  g.appendChild(lbl);
  let el;
  if (f.type === 'select') {
    el = document.createElement('select');
    el.id = f.id;
    f.options.forEach(o => {
      const opt = document.createElement('option');
      opt.value = o;
      opt.textContent = o === 'true' ? 'Yes' : o === 'false' ? 'No' : o;
      el.appendChild(opt);
    });
  } else if (f.type === 'textarea') {
    el = document.createElement('textarea');
    el.id = f.id;
    el.rows = f.rows || 3;
    el.placeholder = f.placeholder || '';
  } else {
    el = document.createElement('input');
    el.type = f.type;
    el.id = f.id;
    el.placeholder = f.placeholder || '';
  }
  if (f.required) el.required = true;
  g.appendChild(el);
  return g;
}

function closeModal() {
  document.getElementById('modal-backdrop').classList.remove('open');
  if (currentEventSource) { currentEventSource.close(); currentEventSource = null; }
  activeReport = null;
  hideFieldTip();
}

// -- Field tooltip floating panel --------------------------------------------
let _tipEl = null;
function _ensureTipEl() {
  if (!_tipEl) {
    _tipEl = document.createElement('div');
    _tipEl.id = 'field-tip-panel';
    document.body.appendChild(_tipEl);
  }
  return _tipEl;
}
function showFieldTip(e, text) {
  const el = _ensureTipEl();
  el.textContent = text;
  el.classList.add('visible');
  positionFieldTip(e, el);
}
function positionFieldTip(e, el) {
  el.style.visibility = 'hidden';
  el.style.display = 'block';
  const rect = e.currentTarget.getBoundingClientRect();
  const panelRect = el.getBoundingClientRect();
  let top = rect.bottom + window.scrollY + 8;
  let left = rect.left + window.scrollX - 8;
  if (left + panelRect.width > window.innerWidth - 16) {
    left = window.innerWidth - panelRect.width - 16;
  }
  if (left < 8) left = 8;
  if (top + panelRect.height > window.innerHeight + window.scrollY - 16) {
    top = rect.top + window.scrollY - panelRect.height - 8;
  }
  el.style.top = top + 'px';
  el.style.left = left + 'px';
  el.style.visibility = 'visible';
}
function hideFieldTip() {
  if (_tipEl) _tipEl.classList.remove('visible');
}

// -- Generate ----------------------------------------------------------------
function resetProgress() {
  document.getElementById('progress-panel').classList.remove('active');
  document.getElementById('progress-log').innerHTML = '';
  document.getElementById('result-bar').classList.remove('show');
  document.querySelectorAll('.step-dot').forEach(d => d.classList.remove('active', 'done'));
  document.getElementById('btn-generate').disabled = false;
}

function collectFormData() {
  const data = {};
  document.getElementById('report-form').querySelectorAll('input, select, textarea').forEach(el => {
    let val = el.value.trim();
    if (el.type === 'number') val = val ? Number(val) : 0;
    if (val === 'true') val = true;
    if (val === 'false') val = false;
    data[el.id] = val;
  });
  return data;
}

function setStep(n) {
  document.querySelectorAll('.step-dot').forEach((d, i) => {
    d.classList.remove('active', 'done');
    if (i < n - 1) d.classList.add('done');
    else if (i === n - 1) d.classList.add('active');
  });
}

function addLogLine(type, message) {
  const log = document.getElementById('progress-log');
  const line = document.createElement('div');
  line.className = `log-line type-${type}`;
  const now = new Date().toLocaleTimeString('en-GB', { hour12: false });
  line.innerHTML = `<span class="log-time">${now}</span><span>${message}</span>`;
  log.appendChild(line);
  log.scrollTop = log.scrollHeight;
}

async function generate() {
  if (!activeReport) return;
  const data = collectFormData();
  const form = document.getElementById('report-form');
  for (const el of form.querySelectorAll('[required]')) {
    if (!el.value.trim()) {
      el.focus();
      el.style.borderColor = 'var(--red)';
      setTimeout(() => el.style.borderColor = '', 2000);
      showToast('Please fill in all required fields', 'error');
      return;
    }
  }
  const noScan = document.getElementById('toggle-no-scan').checked;
  data._no_scan = noScan;
  const rc = _regionCfg();
  data.region = rc.slug;
  data.region_label = rc.label;
  data.region_regulators = rc.regs;
  document.getElementById('btn-generate').disabled = true;
  document.getElementById('progress-panel').classList.add('active');
  document.getElementById('result-bar').classList.remove('show');
  document.getElementById('progress-log').innerHTML = '';
  setStep(1);
  if (currentEventSource) { currentEventSource.close(); currentEventSource = null; }
  try {
    const response = await fetch(`/api/generate/${activeReport.id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop();
      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        try { handleSSEEvent(JSON.parse(line.slice(6))); } catch {}
      }
    }
  } catch (err) {
    addLogLine('error', `Connection error: ${err.message}`);
    document.getElementById('btn-generate').disabled = false;
    showToast('Generation failed -- see log', 'error');
  }
}

function handleSSEEvent(event) {
  switch (event.type) {
    case 'progress':
      addLogLine('progress', event.message);
      if (event.step) setStep(event.step);
      break;
    case 'log':
      addLogLine('log', event.message);
      break;
    case 'complete': {
      addLogLine('complete', event.message);
      setStep(5);
      document.getElementById('btn-generate').disabled = false;
      const bar = document.getElementById('result-bar');
      bar.classList.add('show');
      document.getElementById('result-msg').textContent = event.message;
      const link = document.getElementById('download-link');
      link.href = `/api/download/${event.filename}`;
      link.download = event.filename;
      showToast(`${activeReport.title} ready`, 'success');
      loadRecentReports();
      break;
    }
    case 'error':
      addLogLine('error', event.message);
      document.getElementById('btn-generate').disabled = false;
      showToast(event.message, 'error');
      break;
  }
}

// -- FCA Regulatory Feed -----------------------------------------------------
async function loadFCAUpdates() {
  const feed = document.getElementById('reg-feed');
  const dutyStrip = document.getElementById('duty-strip');
  const dutyRules = document.getElementById('duty-rules');
  if (!feed) return;
  try {
    const res = await fetch('/api/fca-updates');
    if (!res.ok) return;
    const data = await res.json();
    if (data.consumer_duty_obligations?.length) {
      dutyRules.innerHTML = data.consumer_duty_obligations.map(d => `
        <div class="duty-rule">
          <span class="rule-ref">${d.rule}</span>
          <span>${d.obligation}</span>
        </div>`).join('');
      dutyStrip.style.display = 'flex';
    }
    const news = data.news || [];
    if (!news.length) {
      feed.innerHTML = '<div class="reg-item"><div class="reg-dot"></div><div class="reg-body"><div class="reg-headline">No regulatory updates available.</div></div></div>';
      return;
    }
    feed.innerHTML = news.map(n => `
      <div class="reg-item sev-${n.severity}">
        <div class="reg-dot"></div>
        <div class="reg-body">
          <div class="reg-meta">
            <span class="reg-date">${n.date}</span>
            <span class="reg-type">${n.type}</span>
          </div>
          <div class="reg-headline">${n.headline}</div>
          <div class="reg-detail">${n.detail}</div>
          <div class="reg-tags">${(n.tags || []).map(t => `<span class="reg-tag">${t}</span>`).join('')}</div>
        </div>
      </div>`).join('');
    const el = document.getElementById('stat-new-rules');
    if (el && data.new_rules?.length) animateStat(el, data.new_rules.length);
  } catch (e) {
    feed.innerHTML = '<div class="reg-item"><div class="reg-dot"></div><div class="reg-body"><div class="reg-headline" style="color:var(--text-3)">FCA intelligence offline -- start the API server</div></div></div>';
  }
}

// -- Regional Regulatory Feeds -----------------------------------------------
async function loadRegionalFeed(slug, feedId) {
  const feed = document.getElementById(feedId);
  if (!feed) return;
  try {
    const res = await fetch(`/api/regional-updates/${slug}`);
    if (!res.ok) {
      feed.innerHTML = `<div class="reg-item"><div class="reg-dot"></div><div class="reg-body"><div class="reg-headline" style="color:var(--text-3)">${slug} intelligence offline — start the API server</div></div></div>`;
      return;
    }
    const data = await res.json();
    const news = data.news || [];
    if (!news.length) {
      feed.innerHTML = '<div class="reg-item"><div class="reg-dot"></div><div class="reg-body"><div class="reg-headline">No updates available.</div></div></div>';
      return;
    }
    feed.innerHTML = news.map(n => `
      <div class="reg-item sev-${n.severity}">
        <div class="reg-dot"></div>
        <div class="reg-body">
          <div class="reg-meta">
            <span class="reg-date">${n.date}</span>
            ${n.regulator ? `<span class="reg-type">${n.regulator}</span>` : ''}
            ${n.country ? `<span class="reg-country">${n.country}</span>` : ''}
            <span class="reg-type">${n.type}</span>
          </div>
          <div class="reg-headline">${n.headline}</div>
          <div class="reg-detail">${n.detail}</div>
          <div class="reg-tags">${(n.tags || []).map(t => `<span class="reg-tag">${t}</span>`).join('')}</div>
        </div>
      </div>`).join('');
  } catch (e) {
    feed.innerHTML = `<div class="reg-item"><div class="reg-dot"></div><div class="reg-body"><div class="reg-headline" style="color:var(--text-3)">${slug} intelligence offline — start the API server</div></div></div>`;
  }
}

// -- Recent Reports ----------------------------------------------------------
async function loadRecentReports() {
  const tbody = document.getElementById('recent-tbody');
  if (!tbody) return;
  try {
    const res = await fetch('/api/reports');
    const reports = await res.json();
    if (!reports.length) {
      tbody.innerHTML = '<tr><td colspan="4" class="no-reports">No reports generated yet</td></tr>';
      return;
    }
    tbody.innerHTML = reports.map(r => `
      <tr>
        <td>${r.filename.replace('_draft.docx', '').replace(/_/g, ' ')}</td>
        <td>${r.generated}</td>
        <td>${r.size_kb} KB</td>
        <td><a class="btn-dl-sm" href="/api/download/${r.filename}" download="${r.filename}">Download</a></td>
      </tr>`).join('');
    const stat = document.getElementById('stat-reports');
    if (stat) stat.textContent = reports.length;
  } catch (e) {
    tbody.innerHTML = '<tr><td colspan="4" class="no-reports">Error loading reports</td></tr>';
  }
}

// -- Enforcement Fines Panel -------------------------------------------------
async function loadEnforcement() {
  try {
    const res = await fetch('/api/enforcement');
    if (!res.ok) return;
    const items = await res.json();
    if (!items || !items.length) return;

    const title = document.getElementById('enforcement-section-title');
    const grid = document.getElementById('enforcement-grid');
    if (!title || !grid) return;

    title.style.display = 'flex';
    grid.innerHTML = items.slice(0, 12).map(e => {
      const isPending = e.fine.toLowerCase().includes('pending') || e.fine.toLowerCase().includes('n/a') || e.fine.toLowerCase().includes('ban');
      return `
      <div class="enforcement-card">
        <div class="enforcement-firm">${e.firm}</div>
        <div class="enforcement-fine ${isPending ? 'amber' : ''}">${e.fine}</div>
        <div class="enforcement-rules">${(e.rules || []).map(r => `<span class="enforcement-rule-tag">${r}</span>`).join('')}</div>
        <div class="enforcement-summary">${e.summary}</div>
        <div class="enforcement-year">${e.year}</div>
      </div>`;
    }).join('');
  } catch (e) {
    // Enforcement panel is non-critical — fail silently
  }
}

// -- Stat counter animation --------------------------------------------------
function animateStat(el, target) {
  const start = parseInt(el.textContent) || 0;
  if (start === target || isNaN(target)) return;
  const duration = 600;
  const steps = 20;
  const step = (target - start) / steps;
  let current = start;
  let count = 0;
  const id = setInterval(() => {
    count++;
    current += step;
    el.textContent = Math.round(current);
    if (count >= steps) { el.textContent = target; clearInterval(id); }
  }, duration / steps);
}

// -- Toast -------------------------------------------------------------------
function showToast(msg, type = 'info') {
  const stack = document.getElementById('toast-stack');
  const t = document.createElement('div');
  t.className = `toast ${type}`;
  const icon = type === 'success'
    ? `<svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>`
    : type === 'error'
    ? `<svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>`
    : `<svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`;
  t.innerHTML = `${icon} ${msg}`;
  stack.appendChild(t);
  setTimeout(() => t.remove(), 4000);
}

// -- Quick Search (Ctrl+K / Cmd+K) -------------------------------------------
let _qsOpen = false;
let _qsIdx  = -1;

function openQuickSearch() {
  _qsOpen = true;
  _qsIdx  = -1;
  const overlay = document.getElementById('qs-overlay');
  const input   = document.getElementById('qs-input');
  overlay.classList.add('open');
  input.value = '';
  renderQsResults('');
  requestAnimationFrame(() => input.focus());
}

function closeQuickSearch() {
  _qsOpen = false;
  document.getElementById('qs-overlay').classList.remove('open');
}

function renderQsResults(q) {
  const container = document.getElementById('qs-results');
  const term = q.trim().toLowerCase();
  const matches = term
    ? REPORTS.filter(r =>
        r.title.toLowerCase().includes(term) ||
        r.tag.toLowerCase().includes(term) ||
        r.desc.toLowerCase().includes(term) ||
        r.regs.toLowerCase().includes(term)
      )
    : REPORTS;

  if (!matches.length) {
    container.innerHTML = `<div class="qs-empty">No reports match "<em>${q}</em>"</div>`;
    return;
  }

  container.innerHTML = matches.map((r, i) => {
    const hi = s => {
      if (!term) return s;
      const idx = s.toLowerCase().indexOf(term);
      if (idx < 0) return s;
      return s.slice(0, idx) + `<mark class="qs-hl">${s.slice(idx, idx + term.length)}</mark>` + s.slice(idx + term.length);
    };
    return `<div class="qs-item" data-id="${r.id}" data-idx="${i}" tabindex="-1">
      <div class="qs-item-icon ${r.iconClass}">${ICONS[r.icon] || ''}</div>
      <div class="qs-item-body">
        <div class="qs-item-title">${hi(r.title)}</div>
        <div class="qs-item-meta"><span class="card-tag ${r.tagClass}">${r.tag}</span> ${hi(r.desc)}</div>
      </div>
      <div class="qs-item-regs">${r.regs.split(' - ').slice(0, 2).join(' · ')}</div>
    </div>`;
  }).join('');

  container.querySelectorAll('.qs-item').forEach(el => {
    el.addEventListener('mousedown', e => {
      e.preventDefault();
      closeQuickSearch();
      openModal(el.dataset.id);
    });
  });
  _qsIdx = -1;
}

function _qsMove(dir) {
  const items = document.querySelectorAll('.qs-item');
  if (!items.length) return;
  items[_qsIdx < 0 ? 0 : _qsIdx]?.classList.remove('qs-focus');
  _qsIdx = Math.max(0, Math.min(items.length - 1, _qsIdx + dir));
  const active = items[_qsIdx];
  active?.classList.add('qs-focus');
  active?.scrollIntoView({ block: 'nearest' });
}

// -- Daily Intelligence Briefing ---------------------------------------------
let _dailyRunning = false;

const TOPIC_ICONS = {
  // UK
  fca_enforcement:      '⚖',
  cass_updates:         '📋',
  smcr_cocon:           '👤',
  op_resilience:        '🛡',
  client_money_market:  '£',
  consumer_duty:        '🏛',
  ps26_incident:        '📡',
  // North America
  sec_finra:            '🏛',
  us_banking_federal:   '🏦',
  canada_osfi:          '🍁',
  // Latin America
  brazil_cvm:           '🌎',
  mexico_cnbv:          '🌎',
  latam_andes:          '🌎',
  andes_latam:          '🌎',
  // Asia-Pacific
  singapore_mas:        '🌏',
  hong_kong_hkma:       '🌏',
  japan_fsa:            '🌏',
  china_nfra:           '🌏',
  china_csrc:           '🌏',
  india_sebi:           '🌏',
  australia_asic:       '🌏',
  // Africa
  south_africa_fsca:    '🌍',
  nigeria_cbn:          '🌍',
  kenya_east_africa:    '🌍',
};

const REGION_LABELS = {
  'UK':            'UK — FCA · CASS · SM&CR · Operational Resilience',
  'North America': 'North America — USA (Fed · SEC · OCC · FDIC · CFTC · FinCEN · OFAC) · Canada (OSFI · OSC · AMF · FINTRAC)',
  'Latin America': 'Latin America — Brazil (BCB · CVM) · Mexico (BANXICO · CNBV) · Colombia (SFC) · Chile (CMF) · Peru (SBS) · Argentina (BCRA · CNV) · GAFILAT',
  'Asia':          'Asia-Pacific — Singapore (MAS) · Hong Kong (HKMA · SFC) · China (NFRA · CSRC · PBOC) · Japan (FSA) · India (RBI · SEBI) · Australia (ASIC · APRA) · APG',
  'Africa':        'Africa — South Africa (PA/SARB · FSCA Twin Peaks) · Nigeria (CBN) · Kenya (CBK · CMA) · GIABA · ESAAMLG · GABAC',
};

// Region panel metadata — icon, accent colour, regulator short-list, anchor id
const REGIONS_META = {
  'UK': {
    icon: '🇬🇧',
    accent: '#1d6bb5',
    regulators: 'FCA · CASS · SM&CR · Bank of England · CBEST',
    anchorId: 'region-anchor-UK',
  },
  'North America': {
    icon: '🌎',
    accent: '#1a6b3c',
    regulators: 'Fed · SEC · OCC · FDIC · CFTC · FinCEN · OFAC · OSFI · FINTRAC · OSC · AMF',
    anchorId: 'region-anchor-North_America',
  },
  'Latin America': {
    icon: '🌎',
    accent: '#8b6914',
    regulators: 'BCB · CVM · BANXICO · CNBV · SFC · CMF · SBS · BCRA · CNV · GAFILAT',
    anchorId: 'region-anchor-Latin_America',
  },
  'Asia': {
    icon: '🌏',
    accent: '#0e7490',
    regulators: 'MAS · HKMA · SFC · NFRA · CSRC · PBOC · FSA · RBI · SEBI · ASIC · APRA · APG',
    anchorId: 'region-anchor-Asia',
  },
  'Africa': {
    icon: '🌍',
    accent: '#9a3412',
    regulators: 'PA/SARB · FSCA · CBN · CBK · CMA · GIABA · ESAAMLG · GABAC',
    anchorId: 'region-anchor-Africa',
  },
};

function renderRegionsPanel(data) {
  const panel = document.getElementById('regions-panel');
  if (!panel) return;

  const topics = data.topics || [];
  const regionOrder = ['UK', 'North America', 'Latin America', 'Asia', 'Africa'];

  // Group topics by region
  const byRegion = {};
  topics.forEach(t => { const r = t.region || 'UK'; (byRegion[r] = byRegion[r] || []).push(t); });

  panel.innerHTML = regionOrder.map(r => {
    const meta    = REGIONS_META[r] || { icon: '🌐', accent: 'var(--accent)', regulators: r, anchorId: '' };
    const group   = byRegion[r] || [];
    const total   = group.length;
    const scanned = group.filter(t => !t.error).length;
    const failed  = group.filter(t => t.error && t.error !== 'no_scan').length;
    const providers = [...new Set(group.map(t => t.provider).filter(Boolean))];
    const latest  = group.find(t => t.scanned_at);
    const ts      = latest ? _relativeTime(latest.scanned_at) : '';

    let statusCls, statusText;
    if (!total || group.every(t => t.error === 'no_scan')) {
      statusCls = 'rc-status--idle';  statusText = 'Not yet run';
    } else if (failed > 0 && scanned === 0) {
      statusCls = 'rc-status--error'; statusText = 'Scan failed';
    } else if (failed > 0) {
      statusCls = 'rc-status--partial'; statusText = `${scanned}/${total} scanned`;
    } else {
      statusCls = 'rc-status--live';  statusText = 'Live';
    }

    // First valid summary snippet
    const snippetTopic = group.find(t => t.summary && !t.error);
    const snippet = snippetTopic
      ? snippetTopic.summary.split('\n').find(l => l.trim()) || ''
      : '';

    return `<div class="region-card" data-region="${r}"
        style="--rc-accent:${meta.accent}"
        onclick="scrollToRegion('${r}')">
      <div class="rc-icon">${meta.icon}</div>
      <div class="rc-body">
        <div class="rc-header">
          <span class="rc-name">${r}</span>
          <span class="rc-badge">${total} topics</span>
        </div>
        <div class="rc-regulators">${meta.regulators}</div>
        <div class="rc-meta">
          ${ts ? `<span class="rc-ts">${ts}</span>` : ''}
          ${providers.length ? `<span class="rc-providers-used">via ${providers.join(', ')}</span>` : ''}
        </div>
        <span class="rc-status ${statusCls}">${statusText}</span>
        ${snippet ? `<div class="rc-snippet">${snippet.replace(/^[•\-*]\s*/, '').slice(0, 120)}…</div>` : ''}
      </div>
    </div>`;
  }).join('');
}

function scrollToRegion(region) {
  setActiveRegionTab(region);
  const grid = document.getElementById('briefing-grid');
  if (grid) grid.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function _relativeTime(isoStr) {
  if (!isoStr) return '';
  const diff = Date.now() - new Date(isoStr).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1)  return 'just now';
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24)  return `${hrs}h ago`;
  return `${Math.floor(hrs / 24)}d ago`;
}

async function loadDailyBriefing() {
  try {
    const res = await fetch('/api/daily-briefing');
    if (!res.ok) return;
    const data = await res.json();
    renderDailyBriefing(data);
  } catch (e) {
    // Not yet run — show empty state (already in HTML)
  }
}

const RISK_LEVEL_CLS = { HIGH: 'risk-high', MEDIUM: 'risk-medium', LOW: 'risk-low' };

function _renderTopicCard(t) {
  const icon = TOPIC_ICONS[t.id] || '●';
  const hasError = t.error && t.error !== 'no_scan';
  const region = t.region || 'UK';

  const providerBadge = t.provider
    ? `<span class="briefing-provider">${t.provider}</span>`
    : (t.error === 'no_scan' ? '<span class="briefing-provider muted">offline</span>' : '');
  const enrichBadge = t.enriched_by
    ? `<span class="briefing-provider enriched">+ ${t.enriched_by}</span>`
    : '';
  const riskBadge = t.risk_level
    ? `<span class="risk-badge ${RISK_LEVEL_CLS[t.risk_level] || ''}">${t.risk_level}</span>`
    : '';
  const deadlineBadge = t.compliance_deadline
    ? `<span class="briefing-deadline"><span class="briefing-deadline-label">Deadline</span> ${t.compliance_deadline}</span>`
    : '';
  const citationLinks = (t.citations || []).slice(0, 3).map((_, i) =>
    `<span class="briefing-citation">[${i + 1}]</span>`
  ).join('');

  // DeepSeek insight block (shown above raw summary if present)
  const insightHtml = t.insight
    ? `<div class="briefing-insight">${t.insight}</div>`
    : '';

  // Key actions checklist (from DeepSeek enrichment)
  const actionsHtml = t.key_actions?.length
    ? `<ul class="briefing-actions">${t.key_actions.map(a => `<li>${a}</li>`).join('')}</ul>`
    : '';

  // Raw summary lines
  const summary = t.summary || 'No data available.';
  const lines = summary.split('\n').filter(l => l.trim()).map(l =>
    l.startsWith('•') || l.startsWith('-') || l.startsWith('*')
      ? `<li>${l.replace(/^[•\-*]\s*/, '')}</li>`
      : `<p>${l}</p>`
  ).join('');

  return `<div class="briefing-card${hasError ? ' briefing-card--error' : ''}" data-region="${region}">
    <div class="briefing-card-head">
      <span class="briefing-icon">${icon}</span>
      <div class="briefing-title-group">
        <span class="briefing-card-title">${t.title}</span>
        ${riskBadge ? `<div class="briefing-risk-row">${riskBadge}</div>` : ''}
        ${deadlineBadge ? `<div class="briefing-deadline-row">${deadlineBadge}</div>` : ''}
        <div class="briefing-status-row"><span class="briefing-status-label">Status</span><span class="briefing-status-chip">⏱ ${t.status || 'Ongoing'}</span></div>
      </div>
      <span class="briefing-card-meta">${citationLinks}</span>
    </div>
    ${insightHtml}
    ${actionsHtml}
    <div class="briefing-card-body${t.insight ? ' briefing-card-body--secondary' : ''}">${lines || summary}</div>
  </div>`;
}

function setActiveRegionTab(region) {
  // Update tab active state
  document.querySelectorAll('.region-tab').forEach(t => {
    t.classList.toggle('active', t.dataset.region === region);
  });
  // Show/hide region labels and topic cards
  const grid = document.getElementById('briefing-grid');
  if (!grid) return;
  grid.querySelectorAll('.briefing-region-label').forEach(el => {
    el.style.display = (region === 'all' || el.dataset.region === region) ? '' : 'none';
  });
  grid.querySelectorAll('.briefing-card').forEach(el => {
    el.style.display = (region === 'all' || el.dataset.region === region) ? '' : 'none';
  });
  // Sync region overview card highlight
  document.querySelectorAll('.region-card[data-region]').forEach(c => {
    c.classList.toggle('active', c.dataset.region === region);
  });
}

function renderDailyBriefing(data) {
  renderRegionsPanel(data);

  const grid = document.getElementById('briefing-grid');
  const ts   = document.getElementById('briefing-ts');
  if (!grid) return;

  if (ts) {
    ts.textContent = data.generated_date
      ? `Updated ${data.generated_date} ${data.generated_time} · ${_relativeTime(data.generated_at)}`
      : '';
  }

  const topics = data.topics || [];

  // Keep stat counters live
  const topicsStat = document.getElementById('stat-topics');
  if (topicsStat && topics.length) animateStat(topicsStat, topics.length);
  if (!topics.length) {
    grid.innerHTML = '<div class="briefing-empty">No intelligence data yet.</div>';
    return;
  }

  // Group topics by region; fall back to UK for legacy data without region field
  const byRegion = {};
  topics.forEach(t => {
    const r = t.region || 'UK';
    (byRegion[r] = byRegion[r] || []).push(t);
  });

  const regionOrder = ['UK', 'North America', 'Latin America', 'Asia', 'Africa'];
  const multiRegion = Object.keys(byRegion).length > 1;
  let html = '';

  regionOrder.forEach(r => {
    const group = byRegion[r];
    if (!group || !group.length) return;
    if (multiRegion) {
      const label = REGION_LABELS[r] || r;
      const anchorId = (REGIONS_META[r] || {}).anchorId || ('region-anchor-' + r.replace(/\s+/g, '_'));
      html += `<div class="briefing-region-label" id="${anchorId}" data-region="${r}">${label}</div>`;
    }
    html += group.map(_renderTopicCard).join('');
  });

  grid.innerHTML = html;
}

async function runDailyUpdate() {
  if (_dailyRunning) return;
  _dailyRunning = true;
  const btn  = document.getElementById('briefing-run-btn');
  const logW = document.getElementById('briefing-log-wrap');
  const log  = document.getElementById('briefing-log');
  if (btn) { btn.disabled = true; btn.textContent = 'Updating…'; }
  if (logW) { logW.style.display = 'block'; }
  if (log)  { log.innerHTML = ''; }

  const _addLine = (type, msg) => {
    if (!log) return;
    const div = document.createElement('div');
    div.className = `briefing-log-line type-${type}`;
    const t = new Date().toLocaleTimeString('en-GB', { hour12: false });
    div.innerHTML = `<span class="log-time">${t}</span><span>${msg}</span>`;
    log.appendChild(div);
    log.scrollTop = log.scrollHeight;
  };

  try {
    const response = await fetch('/api/daily-update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ no_scan: false }),
    });
    const reader  = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop();
      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        try {
          const ev = JSON.parse(line.slice(6));
          _addLine(ev.type, ev.message);
          if (ev.type === 'complete') {
            showToast('Daily intelligence briefing updated', 'success');
            await loadDailyBriefing();
            setTimeout(() => { if (logW) logW.style.display = 'none'; }, 4000);
          }
          if (ev.type === 'error') showToast(ev.message, 'error');
        } catch {}
      }
    }
  } catch (err) {
    _addLine('error', `Connection error: ${err.message}`);
    showToast('Daily update failed', 'error');
  } finally {
    _dailyRunning = false;
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = `<svg width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg> Run Update`;
    }
  }
}

// -- Init --------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
  initFromURL();
  initParticles();
  initClock();
  renderCards();
  renderRegionSelector();
  initFilter();
  updateFilterBadges();
  loadAIStatus();
  loadRecentReports();
  loadFCAUpdates();
  loadRegionalFeed('north-america',  'reg-feed-north-america');
  loadRegionalFeed('latin-america',  'reg-feed-latin-america');
  loadRegionalFeed('asia-pacific',   'reg-feed-asia-pacific');
  loadRegionalFeed('africa',         'reg-feed-africa');
  loadEnforcement();
  loadDailyBriefing();

  const briefingBtn = document.getElementById('briefing-run-btn');
  if (briefingBtn) briefingBtn.addEventListener('click', runDailyUpdate);

  // Region tab bar — delegate clicks to setActiveRegionTab
  const tabBar = document.getElementById('region-tabs-bar');
  if (tabBar) {
    tabBar.addEventListener('click', e => {
      const btn = e.target.closest('.region-tab');
      if (btn) setActiveRegionTab(btn.dataset.region);
    });
  }

  document.getElementById('modal-backdrop').addEventListener('click', e => {
    if (e.target === e.currentTarget) closeModal();
  });
  document.getElementById('btn-close-modal').addEventListener('click', closeModal);
  document.getElementById('btn-generate').addEventListener('click', generate);

  // Quick search trigger button
  document.getElementById('qs-trigger').addEventListener('click', openQuickSearch);

  // Quick search input events
  const qsInput = document.getElementById('qs-input');
  qsInput.addEventListener('input', () => renderQsResults(qsInput.value));
  qsInput.addEventListener('keydown', e => {
    if (e.key === 'ArrowDown') { e.preventDefault(); _qsMove(1); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); _qsMove(-1); }
    else if (e.key === 'Enter') {
      e.preventDefault();
      const focused = document.querySelector('.qs-item.qs-focus') || document.querySelector('.qs-item');
      if (focused) { closeQuickSearch(); openModal(focused.dataset.id); }
    } else if (e.key === 'Escape') { closeQuickSearch(); }
  });

  // Click outside panel to close quick search
  document.getElementById('qs-overlay').addEventListener('mousedown', e => {
    if (e.target === e.currentTarget) closeQuickSearch();
  });

  // Global keyboard shortcuts
  document.addEventListener('keydown', e => {
    // Ctrl+K or Cmd+K → quick search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      if (_qsOpen) closeQuickSearch(); else openQuickSearch();
      return;
    }
    if (e.key === 'Escape') {
      if (_qsOpen) { closeQuickSearch(); return; }
      closeModal();
    }
    if (e.key === 'Enter' && document.getElementById('modal-backdrop').classList.contains('open')) {
      const focused = document.activeElement;
      if (focused && focused.tagName === 'TEXTAREA') return;
      const btn = document.getElementById('btn-generate');
      if (btn && !btn.disabled) { e.preventDefault(); generate(); }
    }
  });

  setInterval(loadAIStatus, 30000);
  setInterval(loadFCAUpdates, 300000);

  const tickerDate = document.getElementById('ticker-date');
  if (tickerDate) tickerDate.textContent = new Date().toLocaleDateString('en-GB',{day:'2-digit',month:'short',year:'numeric'});

  const _io = new IntersectionObserver(entries => entries.forEach(e => { if(e.isIntersecting) e.target.classList.add('visible'); }), {threshold:0.08});
  document.querySelectorAll('.fade-in').forEach(el => _io.observe(el));

  _twemoji(document.body);
});
