from django.shortcuts import render
import pickle
import numpy as np
import os
from django.conf import settings
from joblib import dump, load

# redeploy
# with open(os.path.join(settings.STATICFILES_DIRS[0], 'utils/staxifierV3.pkl'), 'rb') as modFile:
#     staxifier = pickle.load(modFile)

# with open(os.path.join(settings.STATICFILES_DIRS[0], 'utils/xScaler.pkl'), 'rb') as scalerFile:
#     xScaler = pickle.load(scalerFile)


staxifier = None
xScaler = None

# def load_staxifier():
#     global staxifier
#     global xScaler
#     if staxifier is None:
#         try:
#             with open(os.path.join(settings.STATICFILES_DIRS[0], 'utils/staxifierV3.pkl'), 'rb') as modFile:
#                 staxifier = pickle.load(modFile)

#             with open(os.path.join(settings.STATICFILES_DIRS[0], 'utils/xScaler.pkl'), 'rb') as scalerFile:
#                 xScaler = pickle.load(scalerFile)
#         except FileNotFoundError:
#             staxifier = None
#         except Exception as e:
#             staxifier = None

# def load_staxifier():
#     global staxifier
#     global xScaler
#     if staxifier is None:
#         try:
#             staxifier = load(os.path.join(settings.STATICFILES_DIRS[0], 'utils/staxifierV3.pkl'))

#             with open(os.path.join(settings.STATICFILES_DIRS[0], 'utils/xscaler.pkl'), 'rb') as scalerFile:
#                 xScaler = pickle.load(scalerFile)
#                 print("i ran")
#         except FileNotFoundError:
#             staxifier = None
#         except Exception as e:
#             staxifier = None

def home(request):
    return render(request, "index.html")

def input(request):
    return render(request, "input.html")

def predict(request):
    if request.method == "POST":

        # modFile = open(os.path.join(settings.STATICFILES_DIRS[0], 'utils/staxifierV4.pkl'), 'rb')
        # staxifier = pickle.load(modFile)
        # modFile.close()

        # scalerFile = open(os.path.join(settings.STATICFILES_DIRS[0], 'utils/xScaler.pkl'), 'rb')
        # xScaler = pickle.load(scalerFile)
        # scalerFile.close()

        staxifier = load(os.path.join(settings.STATICFILES_DIRS[0], 'utils/staxifierV4.joblib'))
        # xScaler = load(os.path.join(settings.STATICFILES_DIRS[0], 'utils/xscaler.joblib'))
        xScaler = load(os.path.join(settings.STATICFILES_DIRS[0], 'utils/xscaler.joblib'))
        
        classes = {
            0: 'Insufficient Weight',
            1: 'Normal Weight',
            2: 'Obesity Type I',
            3: 'Obesity Type II',
            4: 'Obesity Type III',
            5: 'Overweight Level I',
            6: 'Overweight Level II'
        }

        class_explanations = {
    0: {
        'class_name': 'Insufficient Weight',
        'message': 'You are classified as having Insufficient Weight.',
        'description': 'Your body weight is below the normal range, which may indicate malnutrition or certain health conditions. To improve your health, focus on consuming a balanced diet rich in nutrients and engage in regular exercise to build muscle mass and improve overall fitness levels. Consulting with a healthcare professional or a nutritionist can provide personalized advice on how to reach a healthy weight.'
    },
    1: {
        'class_name': 'Normal Weight',
        'message': 'You are classified as having Normal Weight.',
        'description': 'Congratulations! Your body weight falls within the normal range for your height and age. To maintain your health, continue practicing healthy lifestyle habits such as eating a balanced diet, staying physically active, managing stress, and getting regular check-ups.'
    },
    2: {
        'class_name': 'Obesity Type I',
        'message': 'You are classified as having Obesity Type I.',
        'description': 'You are considered to be in the early stages of obesity, which increases your risk of developing various health problems such as heart disease, diabetes, and hypertension. To reduce your risk and improve your health, focus on making gradual changes to your diet and lifestyle, such as reducing calorie intake, increasing physical activity, and seeking support from healthcare professionals or support groups.'
    },
    3: {
        'class_name': 'Obesity Type II',
        'message': 'You are classified as having Obesity Type II.',
        'description': 'You are at a higher risk of developing serious health conditions due to obesity. It is essential to take immediate steps to improve your health by adopting a balanced diet, engaging in regular physical activity, and seeking professional medical guidance. Making sustainable lifestyle changes and seeking support from healthcare professionals or support groups can help you manage and reduce your weight.'
    },
    4: {
        'class_name': 'Obesity Type III',
        'message': 'You are classified as having Obesity Type III.',
        'description': 'You are in the most severe stage of obesity, which significantly increases your risk of developing life-threatening health conditions such as heart disease, stroke, and certain types of cancer. It is crucial to prioritize your health and seek comprehensive medical care to address obesity-related complications. Working with a multidisciplinary healthcare team, including doctors, dietitians, and mental health professionals, can help you develop a personalized treatment plan to manage your weight and improve your overall health and well-being.'
    },
    5: {
        'class_name': 'Overweight Level I',
        'message': 'You are classified as having Overweight Level I.',
        'description': 'You are considered to be overweight, which may increase your risk of developing health problems such as high blood pressure, diabetes, and heart disease. To improve your health, focus on adopting a balanced diet that is rich in fruits, vegetables, whole grains, and lean proteins, while reducing intake of processed foods, sugary beverages, and high-fat foods. Engaging in regular physical activity, such as walking, jogging, or swimming, can also help you manage your weight and improve your overall health.'
    },
    6: {
        'class_name': 'Overweight Level II',
        'message': 'You are classified as having Overweight Level II.',
        'description': 'You are considered to be severely overweight, which significantly increases your risk of developing serious health conditions such as heart disease, stroke, and type 2 diabetes. It is essential to prioritize your health and take proactive steps to manage your weight. Start by making small, sustainable changes to your diet and lifestyle, such as reducing portion sizes, increasing physical activity, and seeking support from healthcare professionals or support groups.'
    }
}

        binaryYesNo = {
            'yes':1,
            'no':0
        }

        binaryGender = {
            'male':1,
            'female':0
        }

        frequency = {
            0: 'no',
            1: 'Sometimes',
            2: 'Frequently',
            3: 'Always'
         }
        
        transport = {
            'Automobile':0,
            'Bike':1,
            'Motorbike':2,
            'Public Transportation':3,
            'Walking':4,
        }

        # destructure the form request
        inputFeatures = []

        gender = binaryGender[request.POST["gender-radio"]]
        inputFeatures.append(gender)

        age = request.POST["age"]
        inputFeatures.append(float(age))

        height = request.POST["height"]
        inputFeatures.append(float(height))

        weight = request.POST["weight"]
        inputFeatures.append(float(weight))

        familyHistory = binaryYesNo[request.POST["familyHistory-radio"]]
        inputFeatures.append(familyHistory)

        favc = binaryYesNo[request.POST["favc-radio"]]
        inputFeatures.append(favc)

        fcvc = request.POST["fcvc"]
        inputFeatures.append(float(fcvc))

        ncp = request.POST["ncp"]
        inputFeatures.append(float(ncp))

        caec = request.POST["caec"]
        inputFeatures.append(float(caec))

        smoke = binaryYesNo[request.POST["smoke-radio"]]
        inputFeatures.append(smoke)

        ch2o = request.POST["ch2o"]
        inputFeatures.append(float(ch2o))

        scc = binaryYesNo[request.POST["scc-radio"]]
        inputFeatures.append(scc)

        faf = request.POST["faf"]
        inputFeatures.append(float(faf))

        tue = request.POST["tue"]
        inputFeatures.append(float(tue))

        calc = request.POST["calc"]
        inputFeatures.append(float(calc))

        mtrans = request.POST["mtrans-radio"]
        inputFeatures.append(float(transport[mtrans]))

        inputFeatures = np.array(inputFeatures)
        inputFeatures = xScaler.transform(inputFeatures.reshape(1, -1))
        print(type(inputFeatures))
        print(type(inputFeatures))
        print(inputFeatures)

        yPredict = staxifier.predict(inputFeatures)
        prediction = class_explanations[yPredict[0]]

        context = {
            'receivedData':request.POST,
            'prediction':prediction, 
        }
        return render(request, 'result.html', context)
