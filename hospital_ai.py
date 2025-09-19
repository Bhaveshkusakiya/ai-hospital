from flask import Flask, render_template, request, jsonify
import os
# import numpy as np
import random
from datetime import datetime

app = Flask(__name__)

class AIHospital:
    def __init__(self):
        self.specialists = {
            'cardiology': {
                'name': 'Dr. Sarah Chen',
                'title': 'AI Cardiologist',
                'expertise': 'Heart Disease Detection, ECG Analysis, Cardiac Risk Assessment',
                'icon': '❤️',
                'color': '#e74c3c'
            },
            'neurology': {
                'name': 'Dr. Michael Rodriguez',
                'title': 'AI Neurologist', 
                'expertise': 'Brain Scan Analysis, Stroke Detection, Neurological Disorders',
                'icon': '🧠',
                'color': '#9b59b6'
            },
            'radiology': {
                'name': 'Dr. Emily Watson',
                'title': 'AI Radiologist',
                'expertise': 'X-Ray Analysis, CT Scan Interpretation, Fracture Detection',
                'icon': '🩻',
                'color': '#3498db'
            },
            'dermatology': {
                'name': 'Dr. James Park',
                'title': 'AI Dermatologist',
                'expertise': 'Skin Cancer Detection, Mole Analysis, Skin Condition Diagnosis',
                'icon': '🔬',
                'color': '#f39c12'
            },
            'ophthalmology': {
                'name': 'Dr. Lisa Thompson',
                'title': 'AI Ophthalmologist',
                'expertise': 'Retinal Analysis, Glaucoma Detection, Eye Disease Diagnosis',
                'icon': '👁️',
                'color': '#2ecc71'
            },
            'pathology': {
                'name': 'Dr. Robert Kim',
                'title': 'AI Pathologist',
                'expertise': 'Tissue Analysis, Cancer Detection, Microscopic Examination',
                'icon': '🔬',
                'color': '#e67e22'
            },
            'orthopedics': {
                'name': 'Dr. Amanda Foster',
                'title': 'AI Orthopedic Surgeon',
                'expertise': 'Bone & Joint Analysis, Sports Injuries, Spine Disorders',
                'icon': '🦴',
                'color': '#34495e'
            },
            'psychiatry': {
                'name': 'Dr. David Kumar',
                'title': 'AI Psychiatrist',
                'expertise': 'Mental Health Assessment, Mood Analysis, Behavioral Patterns',
                'icon': '🧘',
                'color': '#8e44ad'
            },
            'gastroenterology': {
                'name': 'Dr. Maria Santos',
                'title': 'AI Gastroenterologist',
                'expertise': 'Digestive System Analysis, Endoscopy Interpretation, GI Disorders',
                'icon': '🫁',
                'color': '#16a085'
            },
            'pulmonology': {
                'name': 'Dr. John Mitchell',
                'title': 'AI Pulmonologist',
                'expertise': 'Lung Function Analysis, Respiratory Disorders, Chest X-rays',
                'icon': '🫁',
                'color': '#2980b9'
            },
            'endocrinology': {
                'name': 'Dr. Rachel Green',
                'title': 'AI Endocrinologist',
                'expertise': 'Hormone Analysis, Diabetes Management, Thyroid Disorders',
                'icon': '⚗️',
                'color': '#d35400'
            },
            'pediatrics': {
                'name': 'Dr. Alex Johnson',
                'title': 'AI Pediatrician',
                'expertise': 'Child Health Assessment, Growth Analysis, Pediatric Conditions',
                'icon': '👶',
                'color': '#f1c40f'
            }
        }
        
        self.sample_cases = {
            'cardiology': [
                {'condition': 'Normal Heart', 'confidence': 0.92, 'risk': 'Low'},
                {'condition': 'Mild Arrhythmia', 'confidence': 0.87, 'risk': 'Medium'},
                {'condition': 'Coronary Blockage', 'confidence': 0.94, 'risk': 'High'}
            ],
            'neurology': [
                {'condition': 'Normal Brain', 'confidence': 0.89, 'risk': 'Low'},
                {'condition': 'Early Stroke Signs', 'confidence': 0.91, 'risk': 'High'},
                {'condition': 'Mild Cognitive Changes', 'confidence': 0.85, 'risk': 'Medium'}
            ],
            'radiology': [
                {'condition': 'No Fractures', 'confidence': 0.96, 'risk': 'Low'},
                {'condition': 'Hairline Fracture', 'confidence': 0.88, 'risk': 'Medium'},
                {'condition': 'Complete Fracture', 'confidence': 0.93, 'risk': 'High'}
            ],
            'dermatology': [
                {'condition': 'Benign Mole', 'confidence': 0.91, 'risk': 'Low'},
                {'condition': 'Atypical Nevus', 'confidence': 0.84, 'risk': 'Medium'},
                {'condition': 'Suspicious Lesion', 'confidence': 0.89, 'risk': 'High'}
            ],
            'ophthalmology': [
                {'condition': 'Healthy Retina', 'confidence': 0.94, 'risk': 'Low'},
                {'condition': 'Early Glaucoma', 'confidence': 0.86, 'risk': 'Medium'},
                {'condition': 'Diabetic Retinopathy', 'confidence': 0.92, 'risk': 'High'}
            ],
            'pathology': [
                {'condition': 'Normal Tissue', 'confidence': 0.95, 'risk': 'Low'},
                {'condition': 'Inflammatory Changes', 'confidence': 0.87, 'risk': 'Medium'},
                {'condition': 'Malignant Cells', 'confidence': 0.91, 'risk': 'High'}
            ],
            'orthopedics': [
                {'condition': 'Healthy Joints', 'confidence': 0.93, 'risk': 'Low'},
                {'condition': 'Mild Arthritis', 'confidence': 0.88, 'risk': 'Medium'},
                {'condition': 'Severe Joint Damage', 'confidence': 0.91, 'risk': 'High'}
            ],
            'psychiatry': [
                {'condition': 'Normal Mental State', 'confidence': 0.89, 'risk': 'Low'},
                {'condition': 'Mild Anxiety', 'confidence': 0.85, 'risk': 'Medium'},
                {'condition': 'Major Depression', 'confidence': 0.92, 'risk': 'High'}
            ],
            'gastroenterology': [
                {'condition': 'Healthy Digestive System', 'confidence': 0.94, 'risk': 'Low'},
                {'condition': 'Gastritis', 'confidence': 0.87, 'risk': 'Medium'},
                {'condition': 'Peptic Ulcer', 'confidence': 0.90, 'risk': 'High'}
            ],
            'pulmonology': [
                {'condition': 'Normal Lung Function', 'confidence': 0.95, 'risk': 'Low'},
                {'condition': 'Mild Asthma', 'confidence': 0.86, 'risk': 'Medium'},
                {'condition': 'Chronic Bronchitis', 'confidence': 0.89, 'risk': 'High'}
            ],
            'endocrinology': [
                {'condition': 'Normal Hormone Levels', 'confidence': 0.92, 'risk': 'Low'},
                {'condition': 'Pre-diabetes', 'confidence': 0.88, 'risk': 'Medium'},
                {'condition': 'Thyroid Dysfunction', 'confidence': 0.91, 'risk': 'High'}
            ],
            'pediatrics': [
                {'condition': 'Normal Development', 'confidence': 0.94, 'risk': 'Low'},
                {'condition': 'Growth Delay', 'confidence': 0.87, 'risk': 'Medium'},
                {'condition': 'Developmental Concerns', 'confidence': 0.90, 'risk': 'High'}
            ]
        }

    def analyze_case(self, specialty, patient_data=None):
        if specialty not in self.specialists:
            return None
        
        # Simulate AI analysis
        case = random.choice(self.sample_cases[specialty])
        specialist = self.specialists[specialty]
        
        return {
            'specialist': specialist,
            'diagnosis': case['condition'],
            'confidence': case['confidence'],
            'risk_level': case['risk'],
            'recommendations': self.get_recommendations(case['condition'], case['risk']),
            'treatment': self.get_treatment_plan(case['condition'], case['risk']),
            'home_remedies': self.get_home_remedies(case['condition']),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def get_recommendations(self, condition, risk):
        recommendations = {
            'Low': ['Regular monitoring recommended', 'Maintain healthy lifestyle', 'Follow-up in 6 months'],
            'Medium': ['Schedule follow-up in 3 months', 'Consider additional tests', 'Monitor symptoms closely'],
            'High': ['Immediate consultation required', 'Urgent medical attention needed', 'Start treatment protocol']
        }
        return recommendations.get(risk, ['Consult with healthcare provider'])
    
    def get_treatment_plan(self, condition, risk):
        treatments = {
            'Normal Heart': ['Continue current lifestyle', 'Regular exercise', 'Heart-healthy diet'],
            'Mild Arrhythmia': ['Beta-blockers if needed', 'Reduce caffeine', 'Stress management'],
            'Coronary Blockage': ['Antiplatelet therapy', 'Statin medication', 'Cardiac catheterization'],
            'Normal Brain': ['Cognitive exercises', 'Regular sleep schedule', 'Brain-healthy nutrition'],
            'Early Stroke Signs': ['Immediate anticoagulation', 'Blood pressure control', 'Emergency intervention'],
            'Mild Cognitive Changes': ['Cognitive therapy', 'Memory exercises', 'Lifestyle modifications'],
            'No Fractures': ['Continue normal activities', 'Calcium supplements', 'Weight-bearing exercises'],
            'Hairline Fracture': ['Immobilization', 'Pain management', 'Gradual rehabilitation'],
            'Complete Fracture': ['Surgical intervention', 'Cast/splint application', 'Physical therapy'],
            'Benign Mole': ['Regular monitoring', 'Sun protection', 'Annual skin checks'],
            'Atypical Nevus': ['Biopsy consideration', 'Close monitoring', 'Dermatology follow-up'],
            'Suspicious Lesion': ['Immediate biopsy', 'Surgical consultation', 'Oncology referral'],
            'Healthy Retina': ['Regular eye exams', 'UV protection', 'Healthy diet'],
            'Early Glaucoma': ['Eye drops', 'Pressure monitoring', 'Regular ophthalmology visits'],
            'Diabetic Retinopathy': ['Blood sugar control', 'Laser therapy', 'Anti-VEGF injections'],
            'Normal Tissue': ['Continue healthy habits', 'Regular screenings', 'Preventive care'],
            'Inflammatory Changes': ['Anti-inflammatory medication', 'Monitor progression', 'Lifestyle changes'],
            'Malignant Cells': ['Oncology consultation', 'Staging studies', 'Treatment planning'],
            'Healthy Joints': ['Regular exercise', 'Joint-friendly activities', 'Maintain healthy weight'],
            'Mild Arthritis': ['NSAIDs', 'Physical therapy', 'Joint protection'],
            'Severe Joint Damage': ['Disease-modifying drugs', 'Joint replacement consideration', 'Pain management'],
            'Normal Mental State': ['Stress management', 'Regular exercise', 'Social connections'],
            'Mild Anxiety': ['Cognitive behavioral therapy', 'Relaxation techniques', 'Lifestyle modifications'],
            'Major Depression': ['Antidepressant medication', 'Psychotherapy', 'Support groups'],
            'Healthy Digestive System': ['Balanced diet', 'Regular meals', 'Adequate hydration'],
            'Gastritis': ['Proton pump inhibitors', 'Dietary modifications', 'Avoid irritants'],
            'Peptic Ulcer': ['H. pylori treatment', 'Acid suppression', 'Dietary changes'],
            'Normal Lung Function': ['Regular exercise', 'Avoid smoking', 'Clean air environment'],
            'Mild Asthma': ['Bronchodilators', 'Inhaled corticosteroids', 'Trigger avoidance'],
            'Chronic Bronchitis': ['Bronchodilators', 'Pulmonary rehabilitation', 'Smoking cessation'],
            'Normal Hormone Levels': ['Balanced diet', 'Regular exercise', 'Stress management'],
            'Pre-diabetes': ['Lifestyle modifications', 'Weight management', 'Regular monitoring'],
            'Thyroid Dysfunction': ['Hormone replacement', 'Regular monitoring', 'Dietary adjustments'],
            'Normal Development': ['Continue current care', 'Regular check-ups', 'Healthy nutrition'],
            'Growth Delay': ['Nutritional assessment', 'Growth hormone evaluation', 'Specialist consultation'],
            'Developmental Concerns': ['Early intervention', 'Developmental therapy', 'Family support']
        }
        return treatments.get(condition, ['Consult with healthcare provider for treatment options'])
    
    def get_home_remedies(self, condition):
        remedies = {
            'Normal Heart': ['30 min daily walk', 'Omega-3 rich foods', 'Meditation 10 min/day'],
            'Mild Arrhythmia': ['Deep breathing exercises', 'Limit caffeine', 'Magnesium-rich foods'],
            'Coronary Blockage': ['Heart-healthy diet', 'Gentle exercise', 'Stress reduction'],
            'Normal Brain': ['Brain games/puzzles', '7-8 hours sleep', 'Blueberries & nuts'],
            'Early Stroke Signs': ['Call emergency services', 'Aspirin if advised', 'Stay calm'],
            'Mild Cognitive Changes': ['Memory games', 'Social activities', 'Mediterranean diet'],
            'No Fractures': ['Calcium-rich foods', 'Vitamin D sunlight', 'Balance exercises'],
            'Hairline Fracture': ['Ice application', 'Elevation', 'Gentle movement'],
            'Complete Fracture': ['Immobilize area', 'Ice packs', 'Seek immediate care'],
            'Benign Mole': ['Sunscreen SPF 30+', 'Monthly self-checks', 'Protective clothing'],
            'Atypical Nevus': ['Daily sunscreen', 'Avoid peak sun hours', 'Regular monitoring'],
            'Suspicious Lesion': ['Protect from sun', 'Document changes', 'Seek medical care'],
            'Healthy Retina': ['Leafy green vegetables', 'Omega-3 foods', 'Regular eye rest'],
            'Early Glaucoma': ['Eye exercises', 'Reduce eye strain', 'Green tea'],
            'Diabetic Retinopathy': ['Blood sugar control', 'Regular eye exams', 'Healthy diet'],
            'Normal Tissue': ['Antioxidant foods', 'Regular exercise', 'Adequate sleep'],
            'Inflammatory Changes': ['Turmeric tea', 'Anti-inflammatory foods', 'Stress reduction'],
            'Malignant Cells': ['Immune-boosting foods', 'Stress management', 'Support groups'],
            'Healthy Joints': ['Gentle stretching', 'Swimming', 'Anti-inflammatory foods'],
            'Mild Arthritis': ['Warm compresses', 'Turmeric supplements', 'Gentle yoga'],
            'Severe Joint Damage': ['Heat/cold therapy', 'Joint protection', 'Weight management'],
            'Normal Mental State': ['Regular exercise', 'Mindfulness practice', 'Social connections'],
            'Mild Anxiety': ['Deep breathing', 'Chamomile tea', 'Regular sleep schedule'],
            'Major Depression': ['Sunlight exposure', 'Regular exercise', 'Support network'],
            'Healthy Digestive System': ['Fiber-rich foods', 'Probiotics', 'Regular meals'],
            'Gastritis': ['Ginger tea', 'Avoid spicy foods', 'Small frequent meals'],
            'Peptic Ulcer': ['Honey', 'Avoid NSAIDs', 'Stress management'],
            'Normal Lung Function': ['Deep breathing exercises', 'Clean air', 'Regular cardio'],
            'Mild Asthma': ['Steam inhalation', 'Avoid triggers', 'Breathing exercises'],
            'Chronic Bronchitis': ['Honey & ginger', 'Humidifier use', 'Quit smoking'],
            'Normal Hormone Levels': ['Balanced nutrition', 'Regular sleep', 'Stress management'],
            'Pre-diabetes': ['Cinnamon tea', 'Low glycemic foods', 'Regular exercise'],
            'Thyroid Dysfunction': ['Iodine-rich foods', 'Selenium supplements', 'Stress reduction'],
            'Normal Development': ['Nutritious meals', 'Active play', 'Adequate sleep'],
            'Growth Delay': ['Protein-rich foods', 'Calcium sources', 'Regular exercise'],
            'Developmental Concerns': ['Stimulating activities', 'Reading together', 'Consistent routine']
        }
        return remedies.get(condition, ['Maintain healthy lifestyle', 'Consult healthcare provider', 'Stay hydrated'])
    
    def get_ai_response(self, message):
        # AI Doctor Chat System
        responses = {
            'fever': "I understand you're experiencing fever. This could indicate your body is fighting an infection. For immediate relief: 1) Take paracetamol as per dosage, 2) Stay hydrated with water and ORS, 3) Use cool compresses, 4) Rest in a cool room. If fever exceeds 102°F or persists beyond 3 days, please seek immediate medical attention.",
            
            'headache': "Headaches can be concerning. Based on medical protocols: 1) Try a cold compress on your forehead, 2) Ensure you're well-hydrated, 3) Rest in a dark, quiet room, 4) Gentle neck stretches may help. If you experience severe headache with vision changes, nausea, or neck stiffness, seek emergency care immediately.",
            
            'chest pain': "⚠️ IMPORTANT: Chest pain requires immediate attention. Please call 108 (ambulance) if you experience: crushing pain, pain radiating to arm/jaw, shortness of breath, or sweating. For mild chest discomfort: avoid physical exertion, sit upright, and monitor symptoms closely. Do not ignore chest pain - when in doubt, seek emergency care.",
            
            'stomach pain': "Abdominal pain can have various causes. For mild stomach pain: 1) Try the BRAT diet (Bananas, Rice, Applesauce, Toast), 2) Stay hydrated with small sips of water, 3) Apply gentle heat to the area, 4) Avoid solid foods temporarily. Seek immediate care if you have severe pain, vomiting blood, or signs of dehydration.",
            
            'cough': "Persistent cough needs attention. For relief: 1) Honey and warm water, 2) Steam inhalation, 3) Stay hydrated, 4) Avoid irritants like smoke. If cough persists beyond 2 weeks, produces blood, or is accompanied by high fever and difficulty breathing, please consult a doctor immediately.",
            
            'cold': "Common cold symptoms are manageable at home. Treatment approach: 1) Rest and sleep 7-8 hours, 2) Warm salt water gargles, 3) Ginger-honey tea, 4) Steam inhalation twice daily. Most colds resolve in 7-10 days. Consult a doctor if symptoms worsen or you develop high fever.",
            
            'anxiety': "I understand anxiety can be overwhelming. Immediate techniques: 1) Practice 4-7-8 breathing (inhale 4, hold 7, exhale 8), 2) Ground yourself using 5-4-3-2-1 technique, 3) Progressive muscle relaxation, 4) Mindfulness meditation. If anxiety interferes with daily life, please consider speaking with a mental health professional.",
            
            'insomnia': "Sleep difficulties affect overall health. Sleep hygiene tips: 1) Maintain consistent sleep schedule, 2) No screens 1 hour before bed, 3) Cool, dark bedroom environment, 4) Chamomile tea or warm milk. If insomnia persists beyond 2 weeks, it may indicate underlying issues requiring medical evaluation.",
            
            'diabetes': "Diabetes management is crucial for long-term health. Key points: 1) Monitor blood sugar regularly, 2) Follow prescribed medication schedule, 3) Maintain balanced diet with complex carbs, 4) Regular exercise as advised. Emergency signs: excessive thirst, frequent urination, blurred vision - seek immediate medical care.",
            
            'blood pressure': "Blood pressure management is vital. Lifestyle modifications: 1) Reduce sodium intake (<2300mg/day), 2) Regular moderate exercise, 3) Maintain healthy weight, 4) Limit alcohol consumption. Monitor BP regularly and take medications as prescribed. Seek emergency care for readings >180/120."
        }
        
        # Check for keywords in the message
        for keyword, response in responses.items():
            if keyword in message:
                return f"As your AI Doctor, {response}"
        
        # General health advice
        if any(word in message for word in ['pain', 'hurt', 'ache']):
            return "I understand you're experiencing pain. Pain is your body's way of signaling that something needs attention. For general pain management: 1) Rest the affected area, 2) Apply ice for acute injuries or heat for muscle tension, 3) Over-the-counter pain relievers as directed. However, persistent or severe pain requires proper medical evaluation. Please describe your symptoms in more detail so I can provide better guidance."
        
        if any(word in message for word in ['tired', 'fatigue', 'exhausted']):
            return "Fatigue can indicate various conditions. Common causes include: lack of sleep, stress, poor nutrition, or underlying medical conditions. Recommendations: 1) Ensure 7-9 hours of quality sleep, 2) Balanced nutrition with iron-rich foods, 3) Regular exercise, 4) Stress management. If fatigue persists despite lifestyle changes, please consult a healthcare provider for proper evaluation."
        
        if any(word in message for word in ['nausea', 'vomit', 'sick']):
            return "Nausea and vomiting can be distressing. Immediate care: 1) Stay hydrated with small, frequent sips of clear fluids, 2) Try ginger tea or candies, 3) Eat bland foods like crackers, 4) Rest in a comfortable position. Seek immediate medical attention if you experience severe dehydration, blood in vomit, or persistent symptoms."
        
        # Default response
        return "Thank you for sharing your health concern with me. As your AI Doctor, I'm here to help. For the most accurate assessment, please describe your symptoms in detail including: when they started, severity (1-10 scale), what makes them better or worse, and any associated symptoms. Remember, while I can provide guidance, serious symptoms always require in-person medical evaluation. Your health and safety are my priority."

hospital = AIHospital()

@app.route('/')
def index():
    return render_template('hospital_modern.html', specialists=hospital.specialists)

@app.route('/analyze/<specialty>', methods=['POST'])
def analyze(specialty):
    try:
        result = hospital.analyze_case(specialty)
        if result:
            return jsonify({'success': True, 'result': result})
        else:
            return jsonify({'success': False, 'message': 'Invalid specialty'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/emergency')
def emergency():
    return jsonify({
        'message': 'Emergency protocols activated',
        'contact': '911 or your local emergency number',
        'status': 'This is a demo system - seek real medical help for emergencies'
    })

@app.route('/remedies')
def remedies():
    return render_template('remedies.html')

@app.route('/ai-chat')
def ai_chat():
    return render_template('ai_chat.html')

@app.route('/search-remedy')
def search_remedy():
    query = request.args.get('q', '').lower()
    all_remedies = {
        'fever': {
            'name': 'Bukhar (Fever)',
            'symptoms': 'High temperature, chills, sweating',
            'remedies': ['Tulsi ka kadha piye', 'Ginger-honey tea', 'Cold compress on forehead', 'Paracetamol le sakte hai'],
            'hindi': 'बुखार के लिए तुलसी का काढ़ा पिएं'
        },
        'cold': {
            'name': 'Sardi-Jukam (Cold)',
            'symptoms': 'Runny nose, sneezing, cough',
            'remedies': ['Garam paani mein namak daal kar gargle kare', 'Steam inhalation', 'Honey-ginger tea', 'Haldi wala doodh'],
            'hindi': 'सर्दी-जुकाम के लिए भाप लें'
        },
        'headache': {
            'name': 'Sir Dard (Headache)',
            'symptoms': 'Pain in head, sensitivity to light',
            'remedies': ['Mathe par thanda patti rakhe', 'Peppermint oil massage', 'Enough paani piye', 'Dark room mein rest kare'],
            'hindi': 'सिर दर्द के लिए ठंडी पट्टी लगाएं'
        },
        'stomach_pain': {
            'name': 'Pet Dard (Stomach Pain)',
            'symptoms': 'Abdominal pain, nausea',
            'remedies': ['Ajwain ka paani piye', 'Hing with warm water', 'Light khana khaye', 'Pudina ki chai'],
            'hindi': 'पेट दर्द के लिए अजवाइन का पानी पिएं'
        },
        'cough': {
            'name': 'Khansi (Cough)',
            'symptoms': 'Persistent cough, throat irritation',
            'remedies': ['Shahad aur adrak', 'Tulsi leaves chew kare', 'Garam paani gargle', 'Mulethi chuse'],
            'hindi': 'खांसी के लिए शहद और अदरक लें'
        },
        'acidity': {
            'name': 'Acidity (Khatta)',
            'symptoms': 'Heartburn, sour taste',
            'remedies': ['Coconut paani piye', 'Banana khaye', 'Jeera paani', 'Cold milk piye'],
            'hindi': 'एसिडिटी के लिए नारियल पानी पिएं'
        },
        'constipation': {
            'name': 'Kabz (Constipation)',
            'symptoms': 'Difficulty in bowel movement',
            'remedies': ['Subah khali pet paani piye', 'Fiber wala khana', 'Triphala powder', 'Exercise kare'],
            'hindi': 'कब्ज के लिए सुबह खाली पेट पानी पिएं'
        },
        'gas': {
            'name': 'Gas (Bloating)',
            'symptoms': 'Bloating, flatulence',
            'remedies': ['Hing ka paani', 'Fennel seeds chew kare', 'Ginger tea', 'Yoga poses kare'],
            'hindi': 'गैस के लिए हींग का पानी पिएं'
        },
        'nausea': {
            'name': 'Ulti (Nausea)',
            'symptoms': 'Feeling of vomiting, dizziness',
            'remedies': ['Adrak chuse', 'Lemon paani', 'Pudina leaves', 'Small meals le'],
            'hindi': 'उल्टी के लिए अदरक चूसें'
        },
        'insomnia': {
            'name': 'Neend Na Aana (Insomnia)',
            'symptoms': 'Difficulty sleeping, restlessness',
            'remedies': ['Chamomile tea piye', 'Warm milk with haldi', 'Mobile band kare', 'Meditation kare'],
            'hindi': 'नींद के लिए कैमोमाइल चाय पिएं'
        },
        'toothache': {
            'name': 'Daant Dard (Toothache)',
            'symptoms': 'Tooth pain, swelling',
            'remedies': ['Namak paani se gargle', 'Clove oil lagaye', 'Ice pack outside', 'Painkiller le sakte hai'],
            'hindi': 'दांत दर्द के लिए नमक पानी से गरारे करें'
        },
        'skin_rash': {
            'name': 'Khujli (Skin Rash)',
            'symptoms': 'Itching, redness, irritation',
            'remedies': ['Neem ka paani', 'Aloe vera gel lagaye', 'Coconut oil', 'Oatmeal bath le'],
            'hindi': 'खुजली के लिए नीम का पानी लगाएं'
        },
        'joint_pain': {
            'name': 'Jodo ka Dard (Joint Pain)',
            'symptoms': 'Pain in joints, stiffness',
            'remedies': ['Haldi wala doodh', 'Ginger tea', 'Hot compress', 'Light exercise kare'],
            'hindi': 'जोड़ों के दर्द के लिए हल्दी वाला दूध पिएं'
        },
        'weakness': {
            'name': 'Kamzori (Weakness)',
            'symptoms': 'Fatigue, low energy',
            'remedies': ['Dates aur almonds khaye', 'Banana daily', 'Protein rich food', 'Proper rest le'],
            'hindi': 'कमजोरी के लिए खजूर और बादाम खाएं'
        },
        'hair_fall': {
            'name': 'Baal Girna (Hair Fall)',
            'symptoms': 'Excessive hair loss',
            'remedies': ['Coconut oil massage', 'Onion juice lagaye', 'Protein diet le', 'Stress kam kare'],
            'hindi': 'बाल गिरने के लिए नारियल तेल की मालिश करें'
        }
    }
    
    if query:
        filtered = {k: v for k, v in all_remedies.items() if query in k or query in v['name'].lower()}
        return jsonify(filtered)
    
    return jsonify(all_remedies)

@app.route('/chat', methods=['POST'])
def chat_with_ai():
    try:
        data = request.get_json()
        message = data.get('message', '').lower()
        
        # AI Doctor Chat Response System
        response = hospital.get_ai_response(message)
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.now().strftime('%H:%M')
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/emergency-contacts')
def emergency_contacts():
    contacts = {
        'national': {
            'ambulance': '108',
            'police': '100',
            'fire': '101',
            'disaster': '1078'
        },
        'mumbai_government': {
            'kem_hospital': '+91-22-2413-6051',
            'sion_hospital': '+91-22-2409-9000',
            'nair_hospital': '+91-22-2373-4000',
            'ltmg_hospital': '+91-22-2412-6301',
            'jj_hospital': '+91-22-2373-5555',
            'rajawadi_hospital': '+91-22-2507-4444'
        },
        'mumbai_private': {
            'fortis_mulund': '+91-22-6754-4444',
            'apollo_navi_mumbai': '+91-22-7120-0000',
            'kokilaben_hospital': '+91-22-4296-9999',
            'lilavati_hospital': '+91-22-2640-2323',
            'hinduja_hospital': '+91-22-4510-8888',
            'breach_candy': '+91-22-2367-8888'
        },
        'budget_friendly': {
            'bmc_hospitals': '1916',
            'esic_hospitals': '1800-11-2526',
            'railway_hospitals': '+91-22-2262-1111',
            'charitable_trust': '+91-22-2414-3000'
        },
        'helplines': {
            'mental_health': '9152987821',
            'women_helpline': '1091',
            'child_helpline': '1098',
            'senior_citizen': '14567'
        }
    }
    return jsonify(contacts)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print("=" * 60)
    print("         MEDICORE AI HOSPITAL SYSTEM")
    print("    'Healing Hearts, Empowering Lives with AI'")
    print("=" * 60)
    print("Starting AI Hospital System...")
    print(f"Running on port: {port}")
    print("12 AI Specialists + Chat Doctor Available")
    print("Made with Love by Bhavesh Kusakiya")
    print("=" * 60)
    app.run(host='0.0.0.0', port=port, debug=False)