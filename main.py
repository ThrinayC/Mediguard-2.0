from nicegui import ui
import requests
from datetime import datetime
import PyPDF2
import re
import io

# the good gradient ( al at top)
ui.add_head_html("""
<style>
body {
    zoom: 2;   /* try 1.1 → 1.2 depending on how big you want */
}
</style>
""", shared=True)

ui.add_head_html("""
<style>
html, body, .q-page {
    height: 100%;
    margin: 0;
    background: linear-gradient(
        180deg,
        #dbeef6 0%,    /* visible medical blue */
        #e6f2f6 30%,   /* transition blue */
        #f3efe8 55%,   /* neutral bridge */
        #f6e4cf 75%,   /* warm peach */
        #f8dcc0 100%   /* soft orange-beige */
    );
}
                 .home-pill {
    padding: 10px 24px;
    border-radius: 9999px;
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(6px);
    font-weight: 600;
    letter-spacing: 0.04em;
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.home-pill:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.12);
}


/* remove default white panels */
.q-page-container,
.q-tab-panels,
.q-tab-panel {
    background: transparent !important;
}
</style>
""" , shared=True)

# hover blue line 

ui.add_head_html("""
<style>
.nav-link {
    position: relative;
    padding: 8px 12px;
    cursor: pointer;
    font-weight: 500;
}

.nav-link::after {
    content: '';
    position: absolute;
    left: 0;
    bottom: -4px;
    width: 0%;
    height: 2px;
    background-color: #3b82f6; /* soft blue */
    transition: width 0.3s ease;
}

.nav-link:hover::after {
    width: 100%;
}
</style>
""", shared=True)

#pill 

ui.add_head_html("""
<style>
.home-pill {
    padding: 12px 28px;
    border-radius: 9999px;

    /* invisible by default */
    background: rgba(255, 255, 255, 0);
    backdrop-filter: blur(0px);
    -webkit-backdrop-filter: blur(0px);
    border: 1px solid rgba(255, 255, 255, 0);

    box-shadow: none;
    transform: scale(0.96);

    font-weight: 600;
    letter-spacing: 0.05em;
    cursor: pointer;
    user-select: none;

    transition:
        background 0.25s ease,
        backdrop-filter 0.25s ease,
        border 0.25s ease,
        box-shadow 0.25s ease,
        transform 0.2s ease;
}

/* ✨ MATERIALIZE ON HOVER */
.home-pill:hover {
    background: rgba(255, 255, 255, 0.18);
    backdrop-filter: blur(18px) saturate(180%);
    -webkit-backdrop-filter: blur(18px) saturate(180%);

    border: 1px solid rgba(255, 255, 255, 0.35);

    box-shadow:
        inset 0 1px 1px rgba(255, 255, 255, 0.4),
        0 14px 35px rgba(0, 0, 0, 0.12);

    transform: scale(1);
}


</style>
""", shared=True)

# pills motto 

ui.add_head_html("""
<style>
.hero-pill {
    padding: 8px 20px;
    border-radius: 9999px;

    background: white;
    border: 1.5px solid #0f766e;
    color: #0f766e;

    font-size: 13px;
    font-weight: 600;
    cursor: pointer;

    transition:
        background 0.2s ease,
        color 0.2s ease,
        box-shadow 0.2s ease,
        transform 0.15s ease;
}

/* HOVER = light teal (NOT solid) */
.hero-pill:hover:not(.active) {
    background: rgba(15, 118, 110, 0.12);
    box-shadow: 0 6px 14px rgba(15,118,110,0.25);
    transform: translateY(-1px);
}

/* ACTIVE = solid teal */
.hero-pill.active {
    background: #0f766e;
    color: white;
    box-shadow: 0 10px 25px rgba(15,118,110,0.4);
}


</style>
""", shared=True)



# pill animaton 

ui.add_head_html("""
<script>
function popHome(el) {
    el.style.transform = 'scale(0.92)';
    setTimeout(() => {
        el.style.transform = 'scale(1)';
    }, 120);
}
</script>
""", shared=True)

#nav bar height 


ui.add_head_html("""
<style>
.top-nav {
    position: sticky;
    top: 0;
    z-index: 50;

    background: rgba(219, 238, 246, 0.85); /* matches gradient top */
    backdrop-filter: blur(6px);

    padding-top: 4px;
    padding-bottom: 6px;

    box-shadow: 0 1px 0 rgba(0, 0, 0, 0.08); /* thin divider line */
}
</style>
""", shared=True)

#selected pills 

ui.add_head_html("""
<style>
.motto-pill {
    padding: 10px 22px;
    border-radius: 9999px;
    border: 1.5px solid #0f766e;
    color: #0f766e;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.25s ease;
    background: transparent;
}

.motto-pill:hover {
    background: rgba(15, 118, 110, 0.08);
}

/* ACTIVE / SELECTED */
.motto-pill.active {
    background: #0f766e;
    color: white;
    box-shadow: 0 10px 25px rgba(15,118,110,0.35);
}

</style>
""", shared=True)

#yellow pill 

ui.add_head_html("""
<style>
.apollo-btn {
    display: inline-flex;          /* 🔑 not block */
    align-items: center;
    width: fit-content;            /* 🔑 shrink to text */

    padding: 10px 22px;
    border-radius: 9999px;

    background: #f3f4f6;           /* grey pill */
    border: 1.5px solid #e5e7eb;
    color: #374151;

    font-weight: 600;
    font-size: 14px;
    cursor: pointer;

    transition:
        background 0.25s ease,
        box-shadow 0.25s ease,
        transform 0.2s ease;
}

/* arrow */
.apollo-btn::after {
    content: '→';
    margin-left: 10px;
    color: #9ca3af;
    transition: transform 0.25s ease, color 0.25s ease;
}

/* hover */
.apollo-btn:hover {
    background: #facc15;
    box-shadow: 0 10px 24px rgba(250, 204, 21, 0.45);
    transform: translateY(-1px);
}

.apollo-btn:hover::after {
    color: white;
    transform: translateX(4px);
}

</style>
""", shared=True)

# Thyroid-specific styles - IMPROVED & BIGGER
ui.add_head_html("""
<style>
.thyroid-card {
    background: rgba(255, 255, 255, 0.95);
    padding: 48px;
    border-radius: 24px;
    border: 2px solid rgba(15, 118, 110, 0.2);
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    margin-bottom: 32px;
    margin-left: 0;
    margin-right: 0;
    width: 100%;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(12px);
}

.thyroid-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 48px rgba(15, 118, 110, 0.2);
    border-color: rgba(15, 118, 110, 0.4);
}

.section-header {
    font-size: 26px;
    font-weight: 700;
    color: #0f766e;
    margin-bottom: 28px;
    padding-bottom: 14px;
    border-bottom: 3px solid #0f766e;
    letter-spacing: 0.02em;
    text-transform: capitalize;
}

/* Make all input labels and text bigger and bolder */
.thyroid-card .q-field__label,
.thyroid-card label,
.thyroid-card input,
.thyroid-card .q-field__native,
.thyroid-card .q-select__dropdown-icon {
    font-size: 17px !important;
    font-weight: 600 !important;
}

.thyroid-card .q-field__bottom {
    font-size: 14px !important;
    font-weight: 500 !important;
}


.bmi-card {
    padding: 24px;
    border-radius: 16px;
    text-align: center;
    font-weight: 600;
    color: white;
    margin: 20px 0;
    animation: fadeIn 0.3s ease;
    border: 2px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}

@keyframes fadeIn {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
}

.result-display {
    padding: 48px;
    border-radius: 24px;
    text-align: center;
    margin-top: 32px;
    margin-left: auto;
    margin-right: auto;
    max-width: 700px;
    animation: slideUp 0.4s ease;
    border: 2px solid rgba(0, 0, 0, 0.1);
    box-shadow: 0 12px 40px rgba(0,0,0,0.15);
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.risk-gauge {
    font-size: 64px;
    font-weight: bold;
    margin: 16px 0;
}

.predict-btn {
    width: 100%;
    padding: 20px;
    border-radius: 16px;
    background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%);
    color: white;
    font-weight: 700;
    font-size: 18px;
    cursor: pointer;
    transition: all 0.3s ease;
    border: none;
    box-shadow: 0 6px 20px rgba(15, 118, 110, 0.35);
    letter-spacing: 0.03em;
}

.predict-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(15, 118, 110, 0.5);
    background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%);
}

.predict-btn:active {
    transform: translateY(-1px);
}

/* Chatbot styles */
.chatbot-container {
    position: fixed;
    bottom: 24px;
    right: 24px;
    z-index: 1000;
}

.chat-bubble {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 20px rgba(15, 118, 110, 0.4);
    transition: all 0.3s ease;
    font-size: 28px;
}

.chat-bubble:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 30px rgba(15, 118, 110, 0.6);
}

.chat-window {
    position: fixed;
    bottom: 100px;
    right: 24px;
    width: 400px;
    height: 600px;
    background: white;
    border-radius: 20px;
    box-shadow: 0 10px 50px rgba(0,0,0,0.2);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    z-index: 999;
}

.chat-header {
    background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%);
    color: white;
    padding: 20px;
    font-weight: 700;
    font-size: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    background: #f9fafb;
}

.chat-message {
    margin-bottom: 16px;
    animation: messageSlide 0.3s ease;
}

@keyframes messageSlide {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.message-bubble {
    padding: 12px 16px;
    border-radius: 16px;
    font-size: 15px;
    line-height: 1.5;
    display: inline-block;
    max-width: 85%;
}

.message-bubble.bot {
    background: white;
    border: 2px solid #e5e7eb;
    color: #1f2937;
}

.message-bubble.user {
    background: #0f766e;
    color: white;
    float: right;
}

.chat-input-area {
    padding: 16px;
    background: white;
    border-top: 2px solid #e5e7eb;
}
</style>
""", shared=True)

# Global variable to store extracted PDF data
pdf_extracted_data = {}

def extract_data_from_pdf(pdf_content):
    """Extract patient data from PDF using text pattern matching"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # Initialize extracted data with defaults
        extracted = {
            'age': 45,
            'gender': 0,  # Female
            'radiation': 0,
            'family_history': 0,
            'iodine': 0,
            'smoking': 0,
            'diabetes': 0,
            'height_feet': 5,
            'height_inches': 6,
            'weight_kg': 70.0,
            'nodule_size': 0.0,
            'ethnicity': 'Asian'
        }
        
        # Extract age
        age_match = re.search(r'age[:\s]*(\d+)', text, re.IGNORECASE)
        if age_match:
            extracted['age'] = int(age_match.group(1))
        
        # Extract gender
        if re.search(r'\b(male|m)\b', text, re.IGNORECASE) and not re.search(r'\bfemale\b', text, re.IGNORECASE):
            extracted['gender'] = 1
        elif re.search(r'\b(female|f)\b', text, re.IGNORECASE):
            extracted['gender'] = 0
        
        # Extract weight (kg or lbs)
        weight_match = re.search(r'weight[:\s]*(\d+\.?\d*)\s*(kg|lbs)?', text, re.IGNORECASE)
        if weight_match:
            weight = float(weight_match.group(1))
            unit = weight_match.group(2)
            if unit and 'lbs' in unit.lower():
                weight = weight * 0.453592  # Convert lbs to kg
            extracted['weight_kg'] = round(weight, 1)
        
        # Extract height (feet/inches or cm)
        height_ft_match = re.search(r"height[:\s]*(\d+)['\"']?\s*(?:ft|feet)?\s*(\d+)?['\"']?\s*(?:in|inches)?", text, re.IGNORECASE)
        if height_ft_match:
            extracted['height_feet'] = int(height_ft_match.group(1))
            if height_ft_match.group(2):
                extracted['height_inches'] = int(height_ft_match.group(2))
        else:
            # Try cm format
            height_cm_match = re.search(r'height[:\s]*(\d+)\s*cm', text, re.IGNORECASE)
            if height_cm_match:
                total_cm = int(height_cm_match.group(1))
                total_inches = total_cm / 2.54
                extracted['height_feet'] = int(total_inches // 12)
                extracted['height_inches'] = int(total_inches % 12)
        
        # Extract nodule size
        nodule_match = re.search(r'nodule[:\s]*(\d+\.?\d*)\s*(?:cm|mm)?', text, re.IGNORECASE)
        if nodule_match:
            size = float(nodule_match.group(1))
            # Assume mm if > 10, otherwise cm
            if size > 10:
                size = size / 10  # Convert mm to cm
            extracted['nodule_size'] = round(size, 1)
        
        # Extract binary risk factors (Yes/No patterns)
        if re.search(r'radiation[:\s]*(yes|positive|present)', text, re.IGNORECASE):
            extracted['radiation'] = 1
        
        if re.search(r'family\s*history[:\s]*(yes|positive|present)', text, re.IGNORECASE):
            extracted['family_history'] = 1
        
        if re.search(r'iodine\s*deficiency[:\s]*(yes|positive|present)', text, re.IGNORECASE):
            extracted['iodine'] = 1
        
        if re.search(r'smok(ing|er)[:\s]*(yes|positive|current)', text, re.IGNORECASE):
            extracted['smoking'] = 1
        
        if re.search(r'diabetes[:\s]*(yes|positive|present)', text, re.IGNORECASE):
            extracted['diabetes'] = 1
        
        # Extract ethnicity
        for eth in ['African', 'Asian', 'Caucasian', 'Hispanic', 'Middle Eastern']:
            if re.search(rf'\b{eth}\b', text, re.IGNORECASE):
                extracted['ethnicity'] = eth
                break
        
        return extracted
        
    except Exception as e:
        print(f"PDF extraction error: {e}")
        return None
    
# navigation bars 

def navbar():
    with ui.row().classes(
        'top-nav w-full items-center justify-center gap-8'
    ):
        ui.label('Overview').classes('nav-link')
        ui.label('Ask LLM').classes('nav-link').on('click', lambda: ui.navigate.to('/ask-llm'))

        ui.label('AI HEALTH INSIGHT').classes('home-pill').on(
            'click',
            lambda: ui.navigate.to('/')
        )

        ui.label('Workflow').classes('nav-link')
        ui.label('About').classes('nav-link')

def make_card(title, text, features, route, image_url=None):
    card = ui.card().classes(
        'w-[900px] p-8 rounded-2xl shadow-lg'
    ).style('display: none;')

    with card:
        # Top section: text left, image right (if provided)
        if image_url:
            with ui.row().classes('w-full gap-6 items-start mb-4'):
                with ui.column().classes('flex-1'):
                    ui.label(title).classes('text-2xl font-bold mb-3')
                    ui.label(text).classes('text-gray-600 mb-4')
                ui.image(image_url).classes('w-40 h-40 object-contain drop-shadow-xl').style(
                    'flex-shrink: 0; filter: drop-shadow(0 4px 16px rgba(220,38,38,0.25));'
                )
        else:
            ui.label(title).classes('text-2xl font-bold mb-3')
            ui.label(text).classes('text-gray-600 mb-4')

        # Bullet points
        with ui.column().classes('gap-2 mb-6'):
            for feature in features:
                with ui.row().classes('gap-2 items-start'):
                    ui.label('•').classes('text-teal-600 font-bold text-lg')
                    ui.label(feature).classes('text-gray-700 text-sm')

        ui.label('Access Risk').classes(
            'apollo-btn mt-6'
        ).on('click', lambda: ui.navigate.to(route))

    return card

def build_pills_and_cards():
    cards = {}
    pill_elements = {}

    def select_pill(name):
        # deactivate all pills
        for p in pill_elements.values():
            p.classes(remove='active')

        # hide all cards
        for c in cards.values():
            c.style('display: none;')
       
        # activate selected
        pill_elements[name].classes(add='active')
        cards[name].style('display: block;')

    # pills
    with ui.row().classes('w-full justify-center gap-3 mt-3'):
        for label in ['UCI Heart disease', 'Heart questionnaire', 'Diabetes', 'Thyroid']:
            pill = ui.label(label).classes('hero-pill')
            pill.on('click', lambda e, l=label: select_pill(l))

            pill_elements[label] = pill

    # cards
    with ui.column().classes('w-full items-center mt-3'):
        cards['UCI Heart disease'] = make_card(
            'UCI Heart Disease Prediction',
            'Predict the likelihood of heart disease using UCI clinical datasets.',
            [
                'Uses 13 clinical attributes including age, cholesterol, and blood pressure',
                'Machine learning model trained on Cleveland Heart Disease Database',
                'Provides percentage-based risk assessment',
                'Includes analysis of chest pain types and exercise-induced symptoms',
                'Recommends appropriate follow-up based on risk level'
            ],
            '/uci-heart',
            image_url='https://img.freepik.com/free-vector/detailed-vector-illustration-human-heart_1308-180437.jpg?semt=ais_hybrid&w=740&q=80'
        )
        cards['Heart questionnaire'] = make_card(
            'Cardiac Questionnaire',
            'Symptom-based cardiac risk screening through comprehensive questionnaire.',
            [
                'Quick 5-minute symptom assessment',
                'Evaluates chest pain, shortness of breath, and palpitations',
                'Considers lifestyle factors like smoking and exercise habits',
                'Family history and genetic predisposition analysis',
                'Generates personalized cardiovascular health report'
            ],
            '/heart-questionnaire'
        )
        cards['Diabetes'] = make_card(
            'Diabetes Risk Assessment',
            'Analyze glucose levels and lifestyle indicators for diabetes risk.',
            [
                'Evaluates blood glucose patterns and HbA1c levels',
                'BMI and waist circumference risk calculation',
                'Family history and genetic predisposition screening',
                'Lifestyle factors: diet, physical activity, and sleep patterns',
                'Provides prediabetes and Type 2 diabetes risk scores'
            ],
            '/diabetes'
        )
        cards['Thyroid'] = make_card(
            'Thyroid Cancer Risk Detection',
            'Advanced AI-powered thyroid disorder and cancer risk assessment.',
            [
                'Low thyroid level may lead to osteoporosis ( bones turning like chalk)',
                'Thyroid nodule size and characteristics evaluation',
                'BMI, age, gender, and ethnicity-based risk modeling',
                'Family history and lifestyle factor screening',
                'AI chatbot for personalized insights and recommendations'
            ],
            '/thyroid'
        )

    # default
    select_pill('UCI Heart disease')


# ---- HERO SECTION ----

@ui.page('/')
def landing_page():
    navbar()

    with ui.column().classes('w-full items-center mt-8'):
        ui.label('MediguardAI– Smart prediction systems').classes(
            'text-4xl font-bold text-center'
        )
        ui.label(
            'keeping you safe with mass and early prediction systems.'
        ).classes('text-sm text-gray-600 mt-2')

    build_pills_and_cards()

@ui.page('/about')
def about_page():
    navbar()
    
    with ui.column().classes('w-full items-center mt-10 gap-6'):
        ui.label('About MediguardAI').classes('text-4xl font-bold')
        ui.label('Advanced AI-Powered Health Risk Assessment Platform').classes('text-lg text-gray-600')
        
        # Mission Statement Card
        with ui.card().classes('w-[1100px] p-12 rounded-3xl shadow-2xl mb-6'):
            with ui.element('div').classes('thyroid-card'):
                ui.label('Our Mission').classes('section-header')
                ui.label(
                    'MediguardAI is an innovative health technology platform that leverages artificial intelligence '
                    'to provide early disease risk assessment and health screening tools. Our mission is to democratize '
                    'access to preliminary health insights, enabling individuals to take proactive steps toward better health '
                    'through early detection and informed decision-making.'
                ).classes('text-lg text-gray-700 leading-relaxed')
        
        # What We Do Card
        with ui.card().classes('w-[1100px] p-12 rounded-3xl shadow-2xl mb-6'):
            with ui.element('div').classes('thyroid-card'):
                ui.label('What We Do').classes('section-header')
                
                with ui.column().classes('gap-4'):
                    with ui.row().classes('gap-4 items-start'):
                        ui.label('🎯').classes('text-3xl')
                        with ui.column().classes('flex-1'):
                            ui.label('Early Risk Detection').classes('text-xl font-bold text-teal-700 mb-2')
                            ui.label(
                                'We provide AI-powered screening tools that analyze multiple health factors to assess '
                                'disease risk before symptoms appear, enabling early intervention and better outcomes.'
                            ).classes('text-gray-700')
                    
                    with ui.row().classes('gap-4 items-start mt-4'):
                        ui.label('🤖').classes('text-3xl')
                        with ui.column().classes('flex-1'):
                            ui.label('Machine Learning Models').classes('text-xl font-bold text-teal-700 mb-2')
                            ui.label(
                                'Our platform utilizes trained machine learning models on verified medical datasets '
                                'to provide evidence-based risk assessments across multiple health conditions.'
                            ).classes('text-gray-700')
                    
                    with ui.row().classes('gap-4 items-start mt-4'):
                        ui.label('💬').classes('text-3xl')
                        with ui.column().classes('flex-1'):
                            ui.label('AI Health Assistant').classes('text-xl font-bold text-teal-700 mb-2')
                            ui.label(
                                'Get instant answers to your health questions through our conversational AI assistant, '
                                'providing personalized insights and recommendations based on your health data.'
                            ).classes('text-gray-700')
                    
                    with ui.row().classes('gap-4 items-start mt-4'):
                        ui.label('📊').classes('text-3xl')
                        with ui.column().classes('flex-1'):
                            ui.label('Comprehensive Data Analysis').classes('text-xl font-bold text-teal-700 mb-2')
                            ui.label(
                                'We integrate clinical measurements, lifestyle factors, family history, and demographic '
                                'data to provide holistic health risk assessments.'
                            ).classes('text-gray-700')
        
        # Our Prediction Models Card
        with ui.card().classes('w-[1100px] p-12 rounded-3xl shadow-2xl mb-6'):
            with ui.element('div').classes('thyroid-card'):
                ui.label('Our Prediction Models').classes('section-header')
                
                # Model 1: UCI Heart Disease
                with ui.element('div').style(
                    'background: linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 100%); '
                    'padding: 24px; '
                    'border-radius: 16px; '
                    'border: 2px solid #14b8a6; '
                    'margin-bottom: 20px;'
                ):
                    ui.label('UCI Heart Disease Prediction').classes('text-2xl font-bold text-teal-800 mb-3')
                    ui.label('Clinical Dataset-Based Cardiovascular Risk Assessment').classes('text-sm font-semibold text-teal-600 mb-4')
                    
                    with ui.column().classes('gap-2'):
                        ui.label('What it does:').classes('text-lg font-bold text-teal-700')
                        ui.label(
                            'Predicts the likelihood of heart disease using 13 clinical attributes including age, cholesterol levels, '
                            'blood pressure, chest pain type, ECG results, and exercise-induced symptoms.'
                        ).classes('text-gray-700 mb-3')
                        
                        ui.label('Key Features:').classes('text-lg font-bold text-teal-700')
                        with ui.column().classes('gap-1 ml-4'):
                            ui.label('• Trained on Cleveland Heart Disease Database').classes('text-gray-700')
                            ui.label('• Analyzes resting blood pressure, serum cholesterol, and maximum heart rate').classes('text-gray-700')
                            ui.label('• Evaluates ST depression and chest pain patterns').classes('text-gray-700')
                            ui.label('• Provides percentage-based cardiovascular risk score').classes('text-gray-700')
                
                # Model 2: Heart Questionnaire
                with ui.element('div').style(
                    'background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); '
                    'padding: 24px; '
                    'border-radius: 16px; '
                    'border: 2px solid #f59e0b; '
                    'margin-bottom: 20px;'
                ):
                    ui.label('Cardiac Health Questionnaire').classes('text-2xl font-bold text-amber-800 mb-3')
                    ui.label('Symptom-Based Cardiovascular Screening').classes('text-sm font-semibold text-amber-600 mb-4')
                    
                    with ui.column().classes('gap-2'):
                        ui.label('What it does:').classes('text-lg font-bold text-amber-700')
                        ui.label(
                            'Comprehensive symptom-based cardiac risk screening through an interactive questionnaire that evaluates '
                            'chest pain, shortness of breath, palpitations, lifestyle factors, and family history.'
                        ).classes('text-gray-700 mb-3')
                        
                        ui.label('Key Features:').classes('text-lg font-bold text-amber-700')
                        with ui.column().classes('gap-1 ml-4'):
                            ui.label('• 5-minute comprehensive symptom assessment').classes('text-gray-700')
                            ui.label('• Evaluates exercise habits, smoking status, diet quality, and stress levels').classes('text-gray-700')
                            ui.label('• Family history and genetic predisposition analysis').classes('text-gray-700')
                            ui.label('• Generates personalized cardiovascular health report').classes('text-gray-700')
                
                # Model 3: Diabetes
                with ui.element('div').style(
                    'background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); '
                    'padding: 24px; '
                    'border-radius: 16px; '
                    'border: 2px solid #3b82f6; '
                    'margin-bottom: 20px;'
                ):
                    ui.label(' Diabetes Risk Assessment').classes('text-2xl font-bold text-blue-800 mb-3')
                    ui.label('Metabolic Health & Glucose Regulation Screening').classes('text-sm font-semibold text-blue-600 mb-4')
                    
                    with ui.column().classes('gap-2'):
                        ui.label('What it does:').classes('text-lg font-bold text-blue-700')
                        ui.label(
                            'Analyzes blood glucose patterns, HbA1c levels, BMI, waist circumference, and lifestyle indicators '
                            'to assess risk for prediabetes and Type 2 diabetes.'
                        ).classes('text-gray-700 mb-3')
                        
                        ui.label('Key Features:').classes('text-lg font-bold text-blue-700')
                        with ui.column().classes('gap-1 ml-4'):
                            ui.label('• Fasting blood glucose and HbA1c evaluation').classes('text-gray-700')
                            ui.label('• BMI and waist circumference risk calculation').classes('text-gray-700')
                            ui.label('• Physical activity, sleep, and stress assessment').classes('text-gray-700')
                            ui.label('• Family history and gestational diabetes screening').classes('text-gray-700')
                
                # Model 4: Thyroid Cancer (Featured)
                with ui.element('div').style(
                    'background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%); '
                    'padding: 24px; '
                    'border-radius: 16px; '
                    'border: 2px solid #ec4899; '
                    'box-shadow: 0 8px 24px rgba(236, 72, 153, 0.2);'
                ):
                    ui.label(' Thyroid Cancer Risk Detection').classes('text-2xl font-bold text-pink-800 mb-3')
                    ui.label('Advanced AI-Powered Thyroid Assessment with Live Deployment').classes('text-sm font-semibold text-pink-600 mb-4')
                    
                    with ui.column().classes('gap-2'):
                        ui.label('What it does:').classes('text-lg font-bold text-pink-700')
                        ui.label(
                            'Our flagship fully-deployed model that analyzes comprehensive risk factors including radiation exposure, '
                            'thyroid nodule characteristics, BMI, family history, and demographic data to predict thyroid cancer risk.'
                        ).classes('text-gray-700 mb-3')
                        
                        ui.label('Key Features:').classes('text-lg font-bold text-pink-700')
                        with ui.column().classes('gap-1 ml-4'):
                            ui.label('•  Currently Live & Operational').classes('text-pink-700 font-bold')
                            ui.label('• Radiation exposure and iodine deficiency analysis').classes('text-gray-700')
                            ui.label('• Thyroid nodule size and characteristics evaluation').classes('text-gray-700')
                            ui.label('• BMI, age, gender, and ethnicity-based risk modeling').classes('text-gray-700')
                            ui.label('• Integrated AI chatbot for personalized insights').classes('text-gray-700')
                            ui.label('• Direct integration with Apollo247 lab testing').classes('text-gray-700')
                            ui.label('• Real-time risk assessment with percentage scores').classes('text-gray-700')
        
        # Technology Stack Card
        with ui.card().classes('w-[1100px] p-12 rounded-3xl shadow-2xl mb-6'):
            with ui.element('div').classes('thyroid-card'):
                ui.label('Technology & Infrastructure').classes('section-header')
                
                with ui.row().classes('w-full gap-6'):
                    with ui.column().classes('flex-1'):
                        ui.label(' Machine Learning').classes('text-xl font-bold text-teal-700 mb-2')
                        ui.label('Scikit-learn, TensorFlow, and custom algorithms trained on verified medical datasets').classes('text-gray-700')
                    
                    with ui.column().classes('flex-1'):
                        ui.label('Frontend Framework').classes('text-xl font-bold text-teal-700 mb-2')
                        ui.label('NiceGUI with custom glassmorphic UI design for seamless user experience').classes('text-gray-700')
                    
                    with ui.column().classes('flex-1'):
                        ui.label(' Integration').classes('text-xl font-bold text-teal-700 mb-2')
                        ui.label('n8n webhook automation for AI chatbot and data submission workflows').classes('text-gray-700')
        
        # Important Disclaimer Card
        with ui.card().classes('w-[1100px] p-12 rounded-3xl shadow-2xl').style(
            'background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%); '
            'border: 3px solid #ef4444;'
        ):
            with ui.element('div').classes('thyroid-card').style('background: transparent; border: none;'):
                ui.label('⚠️ Important Medical Disclaimer').classes('section-header').style('color: #dc2626; border-color: #dc2626;')
                
                ui.label(
                    'MediguardAI is an educational and screening tool designed for preliminary health risk assessment. '
                    'Our predictions are NOT a substitute for professional medical diagnosis, treatment, or clinical advice. '
                    'All models are trained on publicly available datasets and should be used for informational purposes only.'
                ).classes('text-lg text-red-800 font-semibold leading-relaxed mb-4')
                
                ui.label(
                    'If you receive a moderate or high-risk assessment, we strongly recommend consulting with a qualified '
                    'healthcare professional and obtaining proper clinical testing for accurate diagnosis.'
                ).classes('text-base text-red-700 leading-relaxed')
        
        # Footer
        with ui.row().classes('w-full justify-center gap-4 mt-8 mb-8'):
            ui.label('© 2026 MediguardAI').classes('text-gray-500')
            ui.label('|').classes('text-gray-400')
            ui.label('Early Detection • Better Outcomes').classes('text-gray-500 font-semibold')
def navbar():
    with ui.row().classes(
        'top-nav w-full items-center justify-center gap-8'
    ):
        ui.label('Upload Report').classes('nav-link').on('click', lambda: ui.navigate.to('/upload-report'))
        ui.label('Ask LLM').classes('nav-link').on('click', lambda: ui.navigate.to('/ask-llm'))

        ui.label('AI HEALTH INSIGHT').classes('home-pill').on(
            'click',
            lambda: ui.navigate.to('/')
        )

        ui.label('Workflow').classes('nav-link')
        ui.label('About').classes('nav-link').on('click', lambda: ui.navigate.to('/about'))

@ui.page('/upload-report')
def upload_report_page():
    navbar()
    
    with ui.column().classes('w-full items-center mt-10 gap-6'):
        ui.label('📄 Upload Medical Report').classes('text-3xl font-bold')
        ui.label('Upload your PDF report to auto-fill thyroid assessment').classes('text-sm text-gray-500')
        
        with ui.card().classes('w-[900px] p-12 rounded-3xl shadow-2xl'):
            with ui.element('div').classes('thyroid-card'):
                ui.label('Upload Your Report').classes('section-header')
                
                # Status message area
                status_container = ui.column().classes('w-full gap-3 mb-6')
                
                # ✅ FINAL CORRECT FUNCTION
                def handle_upload(e):
                    global pdf_extracted_data
                    
                    try:
                        # Clear previous status messages
                        status_container.clear()
                        
                        with status_container:
                            ui.label('📤 Processing your PDF...').classes('text-lg font-semibold text-blue-600')
                        
                        # ✅ CORRECT: Access the binary data from e.file._data
                        pdf_content = e.file._data
                        
                        # Extract data from PDF
                        extracted = extract_data_from_pdf(pdf_content)
                        
                        if extracted:
                            pdf_extracted_data = extracted
                            
                            status_container.clear()
                            with status_container:
                                ui.label('✅ PDF processed successfully!').classes('text-lg font-semibold text-green-600')
                                ui.label('📊 Extracted Information:').classes('text-md font-bold text-teal-700 mt-4')
                                
                                # Display extracted data
                                with ui.element('div').style(
                                    'background: #f0fdfa; '
                                    'padding: 20px; '
                                    'border-radius: 12px; '
                                    'border: 2px solid #14b8a6;'
                                ):
                                    ui.label(f"Age: {extracted['age']} years").classes('text-gray-700')
                                    ui.label(f"Gender: {'Male' if extracted['gender'] == 1 else 'Female'}").classes('text-gray-700')
                                    ui.label(f"Height: {extracted['height_feet']}'{extracted['height_inches']}\"").classes('text-gray-700')
                                    ui.label(f"Weight: {extracted['weight_kg']} kg").classes('text-gray-700')
                                    ui.label(f"Nodule Size: {extracted['nodule_size']} cm").classes('text-gray-700')
                                    ui.label(f"Ethnicity: {extracted['ethnicity']}").classes('text-gray-700')
                                    ui.label(f"Radiation Exposure: {'Yes' if extracted['radiation'] else 'No'}").classes('text-gray-700')
                                    ui.label(f"Family History: {'Yes' if extracted['family_history'] else 'No'}").classes('text-gray-700')
                                    ui.label(f"Smoking: {'Yes' if extracted['smoking'] else 'No'}").classes('text-gray-700')
                                    ui.label(f"Diabetes: {'Yes' if extracted['diabetes'] else 'No'}").classes('text-gray-700')
                                
                                ui.label('🔄 Redirecting to assessment page...').classes('text-md font-semibold text-blue-600 mt-4')
                            
                            # Redirect to thyroid page after 2 seconds
                            ui.timer(2.0, lambda: ui.navigate.to('/thyroid'), once=True)
                            
                        else:
                            status_container.clear()
                            with status_container:
                                ui.label('⚠️ Could not extract data from PDF').classes('text-lg font-semibold text-orange-600')
                                ui.label('Please proceed to manual entry').classes('text-sm text-gray-600')
                                
                                ui.button(
                                    'Continue to Manual Entry',
                                    on_click=lambda: ui.navigate.to('/thyroid')
                                ).style(
                                    'background: #0f766e; '
                                    'color: white; '
                                    'padding: 12px 24px; '
                                    'border-radius: 8px; '
                                    'margin-top: 12px;'
                                )
                    
                    except Exception as error:
                        status_container.clear()
                        with status_container:
                            ui.label(f'❌ Error: {str(error)}').classes('text-lg font-semibold text-red-600')
                            ui.label('Please try again or proceed to manual entry').classes('text-sm text-gray-600')
                            
                            # Debug output
                            print(f"\n❌ Upload processing error: {error}")
                            import traceback
                            traceback.print_exc()
                            
                            ui.button(
                                'Continue to Manual Entry',
                                on_click=lambda: ui.navigate.to('/thyroid')
                            ).style(
                                'background: #0f766e; '
                                'color: white; '
                                'padding: 12px 24px; '
                                'border-radius: 8px; '
                                'margin-top: 12px;'
                            )
                
                # PDF Upload area
                with ui.element('div').style(
                    'border: 3px dashed #0f766e; '
                    'border-radius: 16px; '
                    'padding: 40px; '
                    'text-align: center; '
                    'background: rgba(15, 118, 110, 0.05);'
                ):
                    ui.label('📁 Drag & Drop PDF Here').classes('text-2xl font-bold text-teal-700 mb-4')
                    ui.label('or click to browse').classes('text-md text-gray-600 mb-6')
                    
                    ui.upload(
                        on_upload=handle_upload,
                        auto_upload=True,
                        max_files=1
                    ).props('accept=".pdf"').classes('w-full').style(
                        'max-width: 400px; '
                        'margin: 0 auto;'
                    )
                
                ui.label(
                    'Supported format: PDF • Max size: 10MB'
                ).classes('text-xs text-gray-400 text-center mt-4')
                
                # Manual entry option
                ui.label('OR').classes('text-center text-lg font-bold text-gray-500 mt-8 mb-4')
                
                ui.button(
                    'Skip to Manual Entry',
                    on_click=lambda: ui.navigate.to('/thyroid')
                ).style(
                    'width: 100%; '
                    'padding: 16px; '
                    'background: #6b7280; '
                    'color: white; '
                    'border-radius: 12px; '
                    'font-weight: 600;'
                )


@ui.page('/uci-heart')
def uci_heart_page():
    navbar()

    with ui.column().classes('w-full items-center mt-10 gap-6'):
        ui.label(' UCI Heart Disease Prediction').classes('text-3xl font-bold')
        ui.label('Educational screening tool · not a medical diagnosis').classes('text-sm text-gray-500')

        with ui.card().classes('w-[1100px] p-12 rounded-3xl shadow-2xl'):
            
            # Basic Information Section
            with ui.element('div').classes('thyroid-card'):
                ui.label('Basic Information').classes('section-header')

                with ui.row().classes('w-full items-center gap-4 mb-6'):
                    ui.label('Age:').classes('text-xl font-bold min-w-[60px]')
                    age = ui.slider(min=18, max=90, value=50).classes('flex-1')
                    age_value = ui.label('50 years').classes('text-xl font-bold min-w-[90px]')
                
                age.on('update:model-value', lambda e: age_value.set_text(f'{int(e.args)} years'))
                
                ui.label('Age range: 18-90 years').classes('text-base font-semibold text-gray-600 mb-4')
                
                gender = ui.select(
                    {1: 'Male', 0: 'Female'},
                    value=1,
                    label='Gender'
                ).classes('w-full')
            
            # Clinical Measurements Section
            with ui.element('div').classes('thyroid-card'):
                ui.label('Clinical Measurements').classes('section-header')
                
                with ui.row().classes('w-full gap-4'):
                    with ui.column().classes('flex-1'):
                        ui.select(
                            {0: 'Typical Angina', 1: 'Atypical Angina', 2: 'Non-anginal Pain', 3: 'Asymptomatic'},
                            value=0,
                            label='Chest Pain Type'
                        ).classes('w-full')
                        
                        ui.number(
                            label='Resting Blood Pressure (mm Hg)',
                            min=80,
                            max=200,
                            value=120,
                            format='%.0f'
                        ).classes('w-full text-xl py-3')
                        
                        ui.number(
                            label='Serum Cholesterol (mg/dl)',
                            min=100,
                            max=400,
                            value=200,
                            format='%.0f'
                        ).classes('w-full text-xl py-3')
                    
                    with ui.column().classes('flex-1'):
                        ui.select(
                            {0: 'No', 1: 'Yes'},
                            value=0,
                            label='Fasting Blood Sugar > 120 mg/dl?'
                        ).classes('w-full')
                        
                        ui.number(
                            label='Maximum Heart Rate Achieved',
                            min=60,
                            max=220,
                            value=150,
                            format='%.0f'
                        ).classes('w-full text-xl py-3')
                        
                        ui.select(
                            {0: 'No', 1: 'Yes'},
                            value=0,
                            label='Exercise Induced Angina?'
                        ).classes('w-full')
            
            # Additional Factors Section
            with ui.element('div').classes('thyroid-card'):
                ui.label('Additional Factors').classes('section-header')
                
                with ui.row().classes('w-full gap-4'):
                    ui.select(
                        {0: 'Normal', 1: 'ST-T Wave Abnormality', 2: 'Left Ventricular Hypertrophy'},
                        value=0,
                        label='Resting ECG Results'
                    ).classes('flex-1')
                    
                    ui.number(
                        label='ST Depression (mm)',
                        min=0,
                        max=6,
                        value=0,
                        step=0.1,
                        format='%.1f'
                    ).classes('flex-1 text-xl py-3')
            
            # Predict Button
            ui.button(
                'Predict Risk',
                on_click=lambda: ui.notify('UCI Heart Disease module coming soon!', type='info')
            ).classes('predict-btn mt-6')
            
            # Disclaimer
            ui.label(
                'Model based on UCI Heart Disease Dataset. '
                'Educational use only · not a medical diagnosis or clinical advice.'
            ).classes('text-xs text-gray-400 text-center mt-6')

@ui.page('/heart-questionnaire')
def heart_questionnaire_page():
    navbar()

    with ui.column().classes('w-full items-center mt-10 gap-6'):
        ui.label(' Heart Health Questionnaire').classes('text-3xl font-bold')
        ui.label('Symptom-based cardiac risk screening · not a medical diagnosis').classes('text-sm text-gray-500')

        with ui.card().classes('w-[1100px] p-12 rounded-3xl shadow-2xl'):
            
            # Symptoms Section
            with ui.element('div').classes('thyroid-card'):
                ui.label('Symptoms Assessment').classes('section-header')
                
                with ui.row().classes('w-full gap-4'):
                    with ui.column().classes('flex-1'):
                        ui.select(
                            {0: 'Never', 1: 'Rarely', 2: 'Sometimes', 3: 'Often', 4: 'Always'},
                            value=0,
                            label='Do you experience chest pain or discomfort?'
                        ).classes('w-full')
                        
                        ui.select(
                            {0: 'Never', 1: 'Rarely', 2: 'Sometimes', 3: 'Often', 4: 'Always'},
                            value=0,
                            label='Do you feel shortness of breath?'
                        ).classes('w-full')
                        
                        ui.select(
                            {0: 'Never', 1: 'Rarely', 2: 'Sometimes', 3: 'Often', 4: 'Always'},
                            value=0,
                            label='Do you experience heart palpitations?'
                        ).classes('w-full')
                    
                    with ui.column().classes('flex-1'):
                        ui.select(
                            {0: 'Never', 1: 'Rarely', 2: 'Sometimes', 3: 'Often', 4: 'Always'},
                            value=0,
                            label='Do you feel dizzy or lightheaded?'
                        ).classes('w-full')
                        
                        ui.select(
                            {0: 'Never', 1: 'Rarely', 2: 'Sometimes', 3: 'Often', 4: 'Always'},
                            value=0,
                            label='Do you experience unusual fatigue?'
                        ).classes('w-full')
                        
                        ui.select(
                            {0: 'No', 1: 'Yes'},
                            value=0,
                            label='Pain radiating to arm/jaw/back?'
                        ).classes('w-full')
            
            # Lifestyle Factors Section
            with ui.element('div').classes('thyroid-card'):
                ui.label('Lifestyle Factors').classes('section-header')
                
                with ui.row().classes('w-full gap-4'):
                    with ui.column().classes('flex-1'):
                        ui.select(
                            {0: 'Never', 1: 'Former', 2: 'Current (<10/day)', 3: 'Current (>10/day)'},
                            value=0,
                            label='Smoking Status'
                        ).classes('w-full')
                        
                        with ui.row().classes('w-full items-center gap-4 mb-6'):
                            ui.label('Exercise (hrs/week):').classes('text-lg font-semibold min-w-[140px]')
                            exercise = ui.slider(min=0, max=20, value=3).classes('flex-1')
                            exercise_value = ui.label('3 hrs').classes('text-lg font-semibold min-w-[60px]')
                        
                        exercise.on('update:model-value', lambda e: exercise_value.set_text(f'{int(e.args)} hrs'))
                    
                    with ui.column().classes('flex-1'):
                        ui.select(
                            {0: 'Excellent', 1: 'Good', 2: 'Fair', 3: 'Poor'},
                            value=1,
                            label='Diet Quality'
                        ).classes('w-full')
                        
                        ui.select(
                            {0: 'Low', 1: 'Moderate', 2: 'High', 3: 'Very High'},
                            value=1,
                            label='Stress Level'
                        ).classes('w-full')
            
            # Family History Section
            with ui.element('div').classes('thyroid-card'):
                ui.label('Family History').classes('section-header')
                
                with ui.row().classes('w-full gap-4'):
                    ui.select(
                        {0: 'No', 1: 'Yes'},
                        value=0,
                        label='Family history of heart disease?'
                    ).classes('flex-1')
                    
                    ui.select(
                        {0: 'No', 1: 'Yes'},
                        value=0,
                        label='Family history of high blood pressure?'
                    ).classes('flex-1')
                    
                    ui.select(
                        {0: 'No', 1: 'Yes'},
                        value=0,
                        label='Family history of stroke?'
                    ).classes('flex-1')
            
            # Predict Button
            ui.button(
                'Assess Risk',
                on_click=lambda: ui.notify('Heart Questionnaire module coming soon!', type='info')
            ).classes('predict-btn mt-6')
            
            # Disclaimer
            ui.label(
                'Symptom-based assessment tool. '
                'Educational use only · not a medical diagnosis or clinical advice.'
            ).classes('text-xs text-gray-400 text-center mt-6')

@ui.page('/diabetes')
def diabetes_page():
    navbar()

    with ui.column().classes('w-full items-center mt-10 gap-6'):
        ui.label(' Diabetes Risk Assessment').classes('text-3xl font-bold')
        ui.label('Comprehensive diabetes screening · not a medical diagnosis').classes('text-sm text-gray-500')

        with ui.card().classes('w-[1100px] p-12 rounded-3xl shadow-2xl'):
            
            # Basic Information Section
            with ui.element('div').classes('thyroid-card'):
                ui.label('Basic Information').classes('section-header')

                with ui.row().classes('w-full items-center gap-4 mb-6'):
                    ui.label('Age:').classes('text-xl font-bold min-w-[60px]')
                    age = ui.slider(min=18, max=90, value=45).classes('flex-1')
                    age_value = ui.label('45 years').classes('text-xl font-bold min-w-[90px]')
                
                age.on('update:model-value', lambda e: age_value.set_text(f'{int(e.args)} years'))
                
                ui.label('Age range: 18-90 years').classes('text-base font-semibold text-gray-600 mb-4')
                
                gender = ui.select(
                    {1: 'Male', 0: 'Female'},
                    value=0,
                    label='Gender'
                ).classes('w-full')
            
            # Blood Sugar & Metabolic Factors Section
            with ui.element('div').classes('thyroid-card'):
                ui.label('Blood Sugar & Metabolic Factors').classes('section-header')
                
                with ui.row().classes('w-full gap-4'):
                    with ui.column().classes('flex-1'):
                        ui.number(
                            label='Fasting Blood Glucose (mg/dL)',
                            min=50,
                            max=300,
                            value=95,
                            format='%.0f'
                        ).classes('w-full text-xl py-3')
                        
                        ui.number(
                            label='HbA1c Level (%)',
                            min=4.0,
                            max=15.0,
                            value=5.5,
                            step=0.1,
                            format='%.1f'
                        ).classes('w-full text-xl py-3')
                        
                        ui.number(
                            label='BMI',
                            min=15,
                            max=50,
                            value=25,
                            step=0.1,
                            format='%.1f'
                        ).classes('w-full text-xl py-3')
                    
                    with ui.column().classes('flex-1'):
                        ui.number(
                            label='Waist Circumference (cm)',
                            min=50,
                            max=150,
                            value=80,
                            format='%.0f'
                        ).classes('w-full text-xl py-3')
                        
                        ui.select(
                            {0: 'No', 1: 'Yes'},
                            value=0,
                            label='High Blood Pressure?'
                        ).classes('w-full')
                        
                        ui.select(
                            {0: 'No', 1: 'Yes'},
                            value=0,
                            label='High Cholesterol?'
                        ).classes('w-full')
            
            # Lifestyle & Risk Factors Section
            with ui.element('div').classes('thyroid-card'):
                ui.label('Lifestyle & Risk Factors').classes('section-header')
                
                with ui.row().classes('w-full gap-4'):
                    with ui.column().classes('flex-1'):
                        with ui.row().classes('w-full items-center gap-4 mb-6'):
                            ui.label('Physical Activity (days/week):').classes('text-lg font-semibold min-w-[180px]')
                            activity = ui.slider(min=0, max=7, value=3).classes('flex-1')
                            activity_value = ui.label('3 days').classes('text-lg font-semibold min-w-[70px]')
                        
                        activity.on('update:model-value', lambda e: activity_value.set_text(f'{int(e.args)} days'))
                        
                        ui.select(
                            {0: 'No', 1: 'Yes'},
                            value=0,
                            label='Family history of diabetes?'
                        ).classes('w-full')
                    
                    with ui.column().classes('flex-1'):
                        ui.select(
                            {0: 'Never', 1: 'Former', 2: 'Current'},
                            value=0,
                            label='Smoking Status'
                        ).classes('w-full')
                        
                        ui.select(
                            {0: 'No', 1: 'Yes'},
                            value=0,
                            label='Gestational Diabetes History?'
                        ).classes('w-full')
            
            # Sleep & Stress Section
            with ui.element('div').classes('thyroid-card'):
                ui.label('Sleep & Stress').classes('section-header')
                
                with ui.row().classes('w-full gap-4'):
                    with ui.row().classes('flex-1 items-center gap-4'):
                        ui.label('Sleep Duration (hrs/night):').classes('text-lg font-semibold min-w-[160px]')
                        sleep = ui.slider(min=3, max=12, value=7).classes('flex-1')
                        sleep_value = ui.label('7 hrs').classes('text-lg font-semibold min-w-[60px]')
                    
                    sleep.on('update:model-value', lambda e: sleep_value.set_text(f'{int(e.args)} hrs'))
                    
                    ui.select(
                        {0: 'Low', 1: 'Moderate', 2: 'High'},
                        value=1,
                        label='Stress Level'
                    ).classes('flex-1')
            
            # Predict Button
            ui.button(
                'Assess Risk',
                on_click=lambda: ui.notify('Diabetes module coming soon!', type='info')
            ).classes('predict-btn mt-6')
            
            # Disclaimer
            ui.label(
                'Diabetes risk screening tool based on clinical guidelines. '
                'Educational use only · not a medical diagnosis or clinical advice.'
            ).classes('text-xs text-gray-400 text-center mt-6')

@ui.page('/thyroid')
def thyroid_page():
    global pdf_extracted_data
    from models.thyroid_logic import predict_thyroid_risk
    
    navbar()
    
    # Check if we have PDF data
    has_pdf_data = bool(pdf_extracted_data)
    
    with ui.column().classes('w-full items-center mt-10 gap-6'):
        ui.label('🔬 Thyroid Cancer Risk Assessment').classes('text-3xl font-bold')
        ui.label('Educational screening tool · not a medical diagnosis').classes('text-sm text-gray-500')
        
        # Show PDF data indicator
        if has_pdf_data:
            with ui.element('div').style(
                'background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); '
                'padding: 12px 24px; '
                'border-radius: 12px; '
                'border: 2px solid #10b981; '
                'margin-bottom: 12px;'
            ):
                ui.label('✅ Form auto-filled from your uploaded PDF report').classes('text-md font-semibold text-green-800')
        
        with ui.card().classes('w-[1100px] p-12 rounded-3xl shadow-2xl'):
            
            # Get initial values from PDF data or defaults
            initial_age = pdf_extracted_data.get('age', 45) if has_pdf_data else 45
            initial_gender = pdf_extracted_data.get('gender', 0) if has_pdf_data else 0
            initial_radiation = pdf_extracted_data.get('radiation', 0) if has_pdf_data else 0
            initial_family = pdf_extracted_data.get('family_history', 0) if has_pdf_data else 0
            initial_iodine = pdf_extracted_data.get('iodine', 0) if has_pdf_data else 0
            initial_smoking = pdf_extracted_data.get('smoking', 0) if has_pdf_data else 0
            initial_diabetes = pdf_extracted_data.get('diabetes', 0) if has_pdf_data else 0
            initial_height_ft = pdf_extracted_data.get('height_feet', 5) if has_pdf_data else 5
            initial_height_in = pdf_extracted_data.get('height_inches', 6) if has_pdf_data else 6
            initial_weight = pdf_extracted_data.get('weight_kg', 70.0) if has_pdf_data else 70.0
            initial_nodule = pdf_extracted_data.get('nodule_size', 0.0) if has_pdf_data else 0.0
            initial_ethnicity = pdf_extracted_data.get('ethnicity', 'Asian') if has_pdf_data else 'Asian'
            
            # Clear PDF data after using it
            if has_pdf_data:
                pdf_extracted_data = {}
            
            # Basic Information Section
            with ui.element('div').classes('thyroid-card'):
                ui.label('Basic Information').classes('section-header')

                with ui.row().classes('w-full items-center gap-4 mb-6'):
                    ui.label('Age:').classes('text-xl font-bold min-w-[60px]')
                    age = ui.slider(min=18, max=90, value=initial_age).classes('flex-1')
                    age_value = ui.label(f'{initial_age} years').classes('text-xl font-bold min-w-[90px]')
                
                age.on('update:model-value', lambda e: age_value.set_text(f'{int(e.args)} years'))
                
                ui.label('Age range: 18-90 years').classes('text-base font-semibold text-gray-600 mb-4')
                
                gender = ui.select(
                    {1: 'Male', 0: 'Female'},
                    value=initial_gender,
                    label='Gender'
                ).classes('w-full')
            
            # Risk Factors Section
            with ui.element('div').classes('thyroid-card'):
                ui.label('Risk Factors').classes('section-header')
                
                with ui.row().classes('w-full gap-4'):
                    with ui.column().classes('flex-1'):
                        radiation = ui.select(
                            {0: 'No', 1: 'Yes'},
                            value=initial_radiation,
                            label='Past radiation exposure to head/neck?'
                        ).classes('w-full')
                        
                        family_history = ui.select(
                            {0: 'No', 1: 'Yes'},
                            value=initial_family,
                            label='Family history of thyroid disease?'
                        ).classes('w-full')
                        
                        iodine = ui.select(
                            {0: 'No', 1: 'Yes'},
                            value=initial_iodine,
                            label='Iodine deficiency?'
                        ).classes('w-full')
                    
                    with ui.column().classes('flex-1'):
                        smoking = ui.select(
                            {0: 'No', 1: 'Yes'},
                            value=initial_smoking,
                            label='Smoking?'
                        ).classes('w-full')
                        
                        diabetes = ui.select(
                            {0: 'No', 1: 'Yes'},
                            value=initial_diabetes,
                            label='Diabetes?'
                        ).classes('w-full')
            
            # Body Measurements Section
            with ui.element('div').classes('thyroid-card'):
                ui.label('Body Measurements').classes('section-header')
                
                with ui.row().classes('w-full gap-4'):
                    height_feet = ui.number(
                        label='Height (feet)',
                        min=3,
                        max=8,
                        value=initial_height_ft,
                        format='%.0f'
                    ).classes('w-full text-xl py-3')
                    
                    height_inches = ui.number(
                        label='Additional inches',
                        min=0,
                        max=11,
                        value=initial_height_in,
                        format='%.0f'
                    ).classes('w-full text-xl py-3')
                
                weight_kg = ui.number(
                    label='Weight (kg)',
                    min=20,
                    max=200,
                    value=initial_weight,
                    format='%.1f'
                ).classes('w-full text-xl py-3')
                
                # BMI Display
                bmi_display = ui.element('div').classes('bmi-card text-xl font-semibold p-6 rounded-xl text-white text-center')
                with bmi_display:
                    bmi_text = ui.label().classes('text-2xl')
                
                def update_bmi():
                    if height_feet.value is None or height_inches.value is None or weight_kg.value is None:
                        return 25
                    
                    h_m = (height_feet.value * 0.3048) + (height_inches.value * 0.0254)
                    bmi = round(weight_kg.value / (h_m ** 2), 2)
                    
                    if bmi < 18.5:
                        category = "Underweight"
                        color = "#e74c3c"
                    elif bmi < 25:
                        category = "Normal"
                        color = "#2ecc71"
                    elif bmi < 30:
                        category = "Overweight"
                        color = "#f1c40f"
                    else:
                        category = "Obese"
                        color = "#c0392b"
                    
                    bmi_display.style(f'background-color: {color};')
                    bmi_text.set_text(f'BMI: {bmi} ({category})')
                    
                    return bmi
                
                height_feet.on_value_change(lambda: update_bmi())
                height_inches.on_value_change(lambda: update_bmi())
                weight_kg.on_value_change(lambda: update_bmi())
                
                update_bmi()
            
            # Clinical Findings Section
            with ui.element('div').classes('thyroid-card'):
                ui.label('Clinical Findings').classes('section-header')
                
                nodule_size = ui.number(
                    label='Thyroid nodule size (cm)',
                    min=0.0,
                    max=10.0,
                    value=initial_nodule,
                    step=0.1,
                    format='%.1f'
                ).classes('w-full text-xl py-3')
                
                ui.label('If no nodule detected, leave as 0').classes('text-sm font-semibold text-gray-600')
                
                ethnicity = ui.select(
                    ["African", "Asian", "Caucasian", "Hispanic", "Middle Eastern"],
                    value=initial_ethnicity,
                    label='Ethnicity'
                ).classes('w-full')
            
            # [Keep all your existing result display, prediction, and chatbot code...]
            
            # Result Display
            result_container = ui.element('div').classes('w-full flex justify-center').style('display: none;')
            with result_container:
                with ui.column().classes('w-full items-center gap-4'):
                    result_card = ui.element('div').classes('result-display')
                    with result_card:
                        result_emoji = ui.label().classes('text-8xl')
                        result_percentage = ui.label().classes('text-5xl font-bold')
                        result_level = ui.label().classes('text-3xl font-semibold mt-2')
                        result_message = ui.label().classes('text-lg mt-4 max-w-2xl mx-auto')
                    
                    apollo_button = ui.element('a').props('href="https://www.apollo247.com/lab-tests-category/thyroid" target="_blank"').style('display: none; text-decoration: none;')
                    with apollo_button:
                        ui.button('🔬 Get Your Lab Tests at Apollo247').props('flat').style(
                            'background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%); '
                            'color: white; '
                            'font-weight: 700; '
                            'font-size: 18px; '
                            'padding: 20px 40px; '
                            'border-radius: 16px; '
                            'box-shadow: 0 8px 24px rgba(220, 38, 38, 0.4); '
                            'transition: all 0.3s ease;'
                        )
            
            def run_prediction():
                try:
                    bmi = update_bmi()
                    obesity_flag = 1 if bmi >= 30 else 0
                    
                    prob = predict_thyroid_risk(
                        age=int(age.value),
                        gender=gender.value,
                        family_history=family_history.value,
                        radiation_exposure=radiation.value,
                        iodine_deficiency=iodine.value,
                        smoking=smoking.value,
                        obesity=obesity_flag,
                        diabetes=diabetes.value,
                        nodule_size=float(nodule_size.value),
                        ethnicity=ethnicity.value
                    )
                    
                    risk_pct = prob * 100
                    
                    if risk_pct >= 60:
                        emoji = '🚨'
                        level = 'High Risk'
                        bg_color = 'background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); border-color: #ef4444;'
                        message = ('⚠️ High risk detected. We recommend proceeding to clinical assessment '
                                 'with basic thyroid lab tests (TSH, T3, T4).')
                        show_apollo = True
                    elif risk_pct >= 39:
                        emoji = '⚠️'
                        level = 'Moderate Risk'
                        bg_color = 'background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-color: #f59e0b;'
                        message = ('Moderate risk detected. Regular monitoring and lifestyle management are advised.')
                        show_apollo = True
                    else:
                        emoji = '✅'
                        level = 'Low Risk'
                        bg_color = 'background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); border-color: #10b981;'
                        message = 'Low risk detected. Maintain healthy lifestyle and routine check-ups.'
                        show_apollo = False
                    
                    result_card.style(bg_color)
                    result_emoji.set_text(emoji)
                    result_percentage.set_text(f'{risk_pct:.1f}%')
                    result_level.set_text(level)
                    result_message.set_text(message)
                    result_container.style('display: flex;')
                    
                    if show_apollo:
                        apollo_button.style('display: block;')
                    else:
                        apollo_button.style('display: none;')
                    
                    ui.notify(f'Risk assessment complete: {risk_pct:.1f}%', type='positive')
                    
                except Exception as e:
                    ui.notify(f'Error: {str(e)}', type='negative')
                    print(f"Prediction error: {e}")
            
            ui.button(
                'Assess Risk',
                on_click=run_prediction
            ).classes('predict-btn mt-6')
            
            ui.label(
                'Model trained on publicly available thyroid cancer risk dataset. '
                'Educational use only · not a medical diagnosis or clinical advice.'
            ).classes('text-xs text-gray-400 text-center mt-6')


    # AI Chatbot
    add_chatbot(age, gender, radiation, family_history, iodine, smoking, diabetes, 
                height_feet, height_inches, weight_kg, nodule_size, ethnicity)

def add_chatbot(age, gender, radiation, family_history, iodine, smoking, diabetes,
                height_feet, height_inches, weight_kg, nodule_size, ethnicity):
    """Add AI chatbot that collects and sends user data to webhook"""
    
    # Chatbot state
    chat_open = {'value': False}
    messages = []
    
    def add_bot_message(text):
        with messages_column:
            with ui.element('div').classes('chat-message'):
                ui.label(text).classes('message-bubble bot')
        messages.append({'role': 'bot', 'text': text})
        # Scroll to bottom
        ui.run_javascript('document.querySelector(".chat-messages").scrollTop = document.querySelector(".chat-messages").scrollHeight')
    
    def add_user_message(text):
        with messages_column:
            with ui.element('div').classes('chat-message').style('text-align: right;'):
                ui.label(text).classes('message-bubble user')
        messages.append({'role': 'user', 'text': text})
        # Scroll to bottom
        ui.run_javascript('document.querySelector(".chat-messages").scrollTop = document.querySelector(".chat-messages").scrollHeight')
    
    def send_to_webhook():
        try:
            # Calculate BMI
            h_m = (height_feet.value * 0.3048) + (height_inches.value * 0.0254)
            bmi = round(weight_kg.value / (h_m ** 2), 2)
            obesity_flag = 1 if bmi >= 30 else 0
            
            # Calculate risk percentage using the same prediction logic
            from models.thyroid_logic import predict_thyroid_risk
            
            risk_prob = predict_thyroid_risk(
                age=int(age.value),
                gender=gender.value,
                family_history=family_history.value,
                radiation_exposure=radiation.value,
                iodine_deficiency=iodine.value,
                smoking=smoking.value,
                obesity=obesity_flag,
                diabetes=diabetes.value,
                nodule_size=float(nodule_size.value),
                ethnicity=ethnicity.value
            )
            
            risk_percentage = round(risk_prob * 100, 2)
            
            # Determine risk level
            if risk_percentage >= 60:
                risk_level = "High Risk"
            elif risk_percentage >= 35:
                risk_level = "Moderate Risk"
            else:
                risk_level = "Low Risk"
            
            # Prepare JSON data payload
            data = {
                "timestamp": datetime.now().isoformat(),
                "patient_data": {
                    "age": int(age.value),
                    "gender": "Male" if gender.value == 1 else "Female",
                    "bmi": bmi,
                    "height_feet": height_feet.value,
                    "height_inches": height_inches.value,
                    "weight_kg": weight_kg.value
                },
                "risk_factors": {
                    "radiation_exposure": bool(radiation.value),
                    "family_history": bool(family_history.value),
                    "iodine_deficiency": bool(iodine.value),
                    "smoking": bool(smoking.value),
                    "diabetes": bool(diabetes.value),
                    "obesity": bool(obesity_flag)
                },
                "clinical_findings": {
                    "nodule_size_cm": float(nodule_size.value),
                    "ethnicity": ethnicity.value
                },
                "risk_assessment": {
                    "risk_percentage": risk_percentage,
                    "risk_level": risk_level,
                    "risk_probability": round(risk_prob, 4)
                }
            }
            
            add_bot_message("📤 Submitting your data...")
            
            # Send JSON to webhook
            webhook_url = "https://vanhellsing.app.n8n.cloud/webhook/submit_diagnosis"
            
            response = requests.post(
                webhook_url,
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                add_bot_message(
                    f"✅ Success! Your assessment data has been submitted.\n\n"
                    f"📊 Risk Assessment: {risk_percentage}% ({risk_level})\n\n"
                    f"Our medical team will review it shortly."
                )
                ui.notify(f'Data submitted successfully! Risk: {risk_percentage}%', type='positive')
            else:
                add_bot_message(
                    f"⚠️ Submission failed (Status: {response.status_code}). Please try again later."
                )
                ui.notify('Submission failed', type='negative')
                
        except requests.exceptions.Timeout:
            add_bot_message("⚠️ Request timed out. Please check your connection and try again.")
            ui.notify('Request timeout', type='warning')
        except Exception as e:
            add_bot_message(f"❌ Error: {str(e)}")
            ui.notify(f'Error: {str(e)}', type='negative')
            print(f"Webhook error: {e}")
    
    def send_message():
        user_msg = message_input.value.strip()
        if not user_msg:
            return
        
        # Add user message
        add_user_message(user_msg)
        message_input.value = ''
        
        # Process message
        user_msg_lower = user_msg.lower()
        
        if any(word in user_msg_lower for word in ['yes', 'submit', 'send', 'sure', 'ok', 'please']):
            # Collect and send data
            send_to_webhook()
        elif any(word in user_msg_lower for word in ['no', 'not', 'cancel']):
            add_bot_message("No problem! Let me know if you need any help.")
        elif 'help' in user_msg_lower:
            add_bot_message(
                "I can help you submit your thyroid assessment data to our system. "
                "Just say 'yes' or 'submit' when you're ready!"
            )
        else:
            add_bot_message(
                "I can submit your current assessment data. Would you like me to do that? "
                "Just say 'yes' or 'submit'!"
            )
    
    def toggle_chat():
        chat_open['value'] = not chat_open['value']
        if chat_open['value']:
            chat_window.style('display: flex;')
            chat_bubble_btn.style('display: none;')
            # Send welcome message
            if len(messages) == 0:
                add_bot_message(
                    "Hello! I'm your MediguardAI assistant. I can help you with your thyroid "
                    "risk assessment. Would you like me to submit your current assessment data?"
                )
        else:
            chat_window.style('display: none;')
            chat_bubble_btn.style('display: flex;')
    
    # Chat window container
    chat_window = ui.element('div').classes('chat-window').style('display: none;')
    
    with chat_window:
        # Header
        with ui.element('div').classes('chat-header'):
            ui.label('🤖 MediguardAI Assistant')
            ui.button('✕', on_click=lambda: toggle_chat()).props('flat dense').style(
                'color: white; font-size: 20px;'
            )
        
        # Messages area
        messages_container = ui.element('div').classes('chat-messages')
        with messages_container:
            messages_column = ui.column().classes('w-full')
        
        # Input area
        with ui.element('div').classes('chat-input-area'):
            with ui.row().classes('w-full gap-2'):
                message_input = ui.input(placeholder='Type your message...').classes('flex-1').on('keydown.enter', send_message)
                ui.button('Send', on_click=send_message).props('flat').style(
                    'background: #0f766e; color: white;'
                )
    
    # Chat bubble button
    chat_bubble_btn = ui.button('💬', on_click=lambda: toggle_chat()).classes('chat-bubble')



@ui.page('/ask-llm')
def ask_llm_page():
    navbar()
    
    with ui.column().classes('w-full items-center mt-10 gap-6'):
        ui.label(' Ask LLM - AI Health Assistant').classes('text-3xl font-bold')
        ui.label('Get instant answers to your health questions').classes('text-sm text-gray-500')
        
        with ui.card().classes('w-[900px] p-12 rounded-3xl shadow-2xl'):
            with ui.element('div').classes('thyroid-card'):
                ui.label('AI Health Chat').classes('section-header')
                
                # Informational message
                with ui.element('div').style(
                    'background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); '
                    'padding: 32px; '
                    'border-radius: 16px; '
                    'border: 2px solid #3b82f6; '
                    'text-align: center; '
                    'margin-bottom: 24px;'
                ):
                    ui.label(' Chat with our AI Health Assistant').classes('text-2xl font-bold text-blue-800 mb-4')
                    ui.label(
                        'Click the button below to open our AI-powered health assistant in a new tab. '
                        'Ask questions about symptoms, conditions, wellness, and get personalized health insights.'
                    ).classes('text-lg text-gray-700 mb-6')
                    
                    # Open chat button
                    # Open chat button
                with ui.link(
                    target='https://vanhellsing.app.n8n.cloud/webhook/4a5b6c7d-8e9f-0123-4567-890abcdef123/chat',
                    new_tab=True
                ).style('text-decoration: none;').classes('w-full'):
                    ui.button(' Open AI Health Chat').style(
                        'width: 100%; '
                        'padding: 20px 40px; '
                        'border-radius: 16px; '
                        'background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%); '
                        'color: white; '
                        'font-weight: 700; '
                        'font-size: 20px; '
                        'cursor: pointer; '
                        'transition: all 0.3s ease; '
                        'border: none; '
                        'box-shadow: 0 6px 20px rgba(15, 118, 110, 0.35);'
                    ).on('mouseenter', lambda: ui.run_javascript(
                        'event.target.style.transform = "translateY(-3px)"; '
                        'event.target.style.boxShadow = "0 12px 32px rgba(15, 118, 110, 0.5)";'
                    )).on('mouseleave', lambda: ui.run_javascript(
                        'event.target.style.transform = "translateY(0)"; '
                        'event.target.style.boxShadow = "0 6px 20px rgba(15, 118, 110, 0.35)";'
                    ))
                
                # Features list
                with ui.element('div').style('margin-top: 32px;'):
                    ui.label('Features:').classes('text-xl font-bold text-teal-700 mb-4')
                    
                    with ui.column().classes('gap-3'):
                        with ui.row().classes('gap-3 items-start'):
                            ui.label('✅').classes('text-2xl')
                            ui.label('24/7 AI-powered health information and guidance').classes('text-gray-700')
                        
                        with ui.row().classes('gap-3 items-start'):
                            ui.label('✅').classes('text-2xl')
                            ui.label('Answers to medical questions and symptom analysis').classes('text-gray-700')
                        
                        with ui.row().classes('gap-3 items-start'):
                            ui.label('✅').classes('text-2xl')
                            ui.label('Personalized health insights and recommendations').classes('text-gray-700')
                        
                        with ui.row().classes('gap-3 items-start'):
                            ui.label('✅').classes('text-2xl')
                            ui.label('Natural conversational interface').classes('text-gray-700')
            
            # Disclaimer
            ui.label(
                '⚠️ Disclaimer: This AI assistant provides general health information only. '
                'Always consult with a qualified healthcare professional for medical advice, diagnosis, or treatment.'
            ).classes('text-xs text-gray-500 text-center mt-6')
            
ui.run(host='0.0.0.0', port=8080)
