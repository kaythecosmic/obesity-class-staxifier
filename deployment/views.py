from django.shortcuts import render
import pickle
import numpy as np
import os
from django.conf import settings
from joblib import dump, load

def home(request):
    return render(request, "index.html")

def input(request):
    return render(request, "input.html")

def predict(request):
    if request.method == "POST":

        staxifier = load(os.path.join(settings.STATICFILES_DIRS[0], 'utils/staxifierV4.joblib'))
        xScaler = load(os.path.join(settings.STATICFILES_DIRS[0], 'utils/xscaler.joblib'))
        
        class_explanations = {
                    0: {
                        'class_name': 'Insufficient Weight',
                        'message': 'You are classified as having Insufficient Weight.',
                        'description': 'Your body weight is below the normal range, which may indicate malnutrition or certain health conditions. To improve your health, focus on consuming a diet with rich nutrients and engage in regular exercise to build muscle mass. Getting guidance from a healthcare professional or a nutritionist can offer tailored recommendations for achieving a healthy weight.'
                    },
                    1: {
                        'class_name': 'Normal Weight',
                        'message': 'You are classified as having Normal Weight.',
                        'description': ' Great job! Your body weight is within the healthy range for your height and age. To keep up your good health, keep following healthy lifestyle habits like eating a balanced diet, staying physically active, managing stress, and getting regular check-ups.'
                    },
                    2: {
                        'class_name': 'Obesity Type I',
                        'message': 'You are classified as having Obesity Type I.',
                        'description': ' You are in the early stages of obesity, which raises the risk of developing health issues like heart disease, diabetes, and hypertension. To lower these risks and enhance your health, start making gradual changes to your diet and lifestyle. This includes reducing calorie intake, increasing physical activity, and seeking guidance from healthcare professionals or support groups.'
                    },
                    3: {
                        'class_name': 'Obesity Type II',
                        'message': 'You are classified as having Obesity Type II.',
                        'description': 'You are at a higher risk of developing serious health conditions due to obesity. It is essential to take immediate steps to improve your health by adopting a balanced diet, engaging in regular physical activity, and seeking professional medical guidance. Making sustainable lifestyle changes and seeking support from healthcare professionals or support groups can help you manage and reduce your weight.'
                    },
                    4: {
                        'class_name': 'Obesity Type III',
                        'message': 'You are classified as having Obesity Type III.',
                        'description': ' You are in the most severe stage of obesity, increasing the risk of life-threatening health issues like heart disease, stroke, and cancer. Prioritize your health by seeking comprehensive medical care. Work with a team of healthcare professionals, including doctors, dietitians, and mental health professionals, to develop a personalized treatment plan for managing your weight and improving your overall well-being.'
                    },
                    5: {
                        'class_name': 'Overweight Level I',
                        'message': 'You are classified as having Overweight Level I.',
                        'description': 'Being overweight can increase your risk of health issues like high blood pressure, diabetes, and heart disease. Improve your health by focusing on a balanced diet with fruits, vegetables, whole grains, and lean proteins, while cutting back on processed foods, sugary beverages, and high-fat foods. Regular physical activity, like walking or swimming, can also help manage your weight and enhance your health.'
                    },
                    6: {
                        'class_name': 'Overweight Level II',
                        'message': 'You are classified as having Overweight Level II.',
                        'description': ' You are severely overweight which raises your risk of serious health issues like heart disease, stroke, and type 2 diabetes. Its important to prioritize your health and take proactive steps to manage your weight. Begin by making small, sustainable changes to your diet and lifestyle, such as reducing portion sizes, increasing physical activity, and seeking guidance from healthcare professionals or support groups.'
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
