from flask import Flask, render_template, request, jsonify, redirect, url_for
import google.generativeai as genai
from dotenv import load_dotenv
import os
# Configure Google API
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

sessionHistory = [
    {
        "role": "user",
        "parts": ["Hi"],
    },
    {
        "role": "model",
        "parts": [
            "Hello! I'm TreeBo, your guide to Sustainable Development Goals and how we can build a better future for everyone. What would you like to learn about today? 😊 \n",
        ],
    },
    {
        "role": "user",
        "parts": ["what are sustainable development goals"],
    },
    {
        "role": "model",
        "parts": [
            "That's a great question! Imagine our planet as a giant puzzle. The Sustainable Development Goals (SDGs) are like the puzzle pieces we need to fit together to create a better, healthier, and more just world for everyone. \n\nHere's the simple breakdown:\n\n* **17 Goals:** There are 17 SDGs, each focusing on a different aspect of our world, like ending poverty, fighting hunger, improving health, protecting the environment, and promoting peace. \n* **Universal:** These goals apply to every country and everyone on Earth. It's a global effort!\n* **Interconnected:** Just like the pieces of a puzzle, these goals are all connected. Solving one problem often helps with others. \n* **Timebound:** The goal is to achieve these by the year 2030. \n\nThink of it this way: \n\n* **Ending poverty** means people have access to basic needs like food, water, and shelter.\n* **Protecting the environment** means we use resources wisely and prevent pollution. \n* **Promoting peace** means building a world where everyone feels safe and respected. \n\nBy working together, we can make sure everyone has the chance to thrive! What specific SDG are you interested in learning more about? 🤔\n",
        ],
    },
    {
        "role": "user",
        "parts": ["List all 17 goals"],
    },
    {
        "role": "model",
        "parts": [
            "You got it! Here are the 17 Sustainable Development Goals, ready to make our world a better place:\n\n**1. No Poverty:** Ending poverty in all its forms everywhere.\n\n**2. Zero Hunger:** Ending hunger, achieving food security and improved nutrition, and promoting sustainable agriculture.\n\n**3. Good Health and Well-being:** Ensuring healthy lives and promoting well-being for all at all ages.\n\n**4. Quality Education:** Ensuring inclusive and equitable quality education and promoting lifelong learning opportunities for all.\n\n**5. Gender Equality:** Achieving gender equality and empowering all women and girls.\n\n**6. Clean Water and Sanitation:** Ensuring availability and sustainable management of water and sanitation for all.\n\n**7. Affordable and Clean Energy:** Ensuring access to affordable, reliable, sustainable and modern energy for all.\n\n**8. Decent Work and Economic Growth:** Promoting sustained, inclusive and sustainable economic growth, full and productive employment and decent work for all.\n\n**9. Industry, Innovation and Infrastructure:** Building resilient infrastructure, promoting inclusive and sustainable industrialization and fostering innovation.\n\n**10. Reduced Inequalities:** Reducing inequality within and among countries.\n\n**11. Sustainable Cities and Communities:** Making cities and human settlements inclusive, safe, resilient and sustainable.\n\n**12. Responsible Consumption and Production:** Ensuring sustainable consumption and production patterns.\n\n**13. Climate Action:** Taking urgent action to combat climate change and its impacts.\n\n**14. Life Below Water:** Conserving and sustainably using the oceans, seas and marine resources for sustainable development.\n\n**15. Life on Land:** Protecting, restoring and promoting sustainable use of terrestrial ecosystems, sustainably managing forests, combating desertification, and halting and reversing land degradation and halting biodiversity loss.\n\n**16. Peace, Justice and Strong Institutions:** Promoting peaceful and inclusive societies for sustainable development, providing access to justice for all and building effective, accountable and inclusive institutions at all levels.\n\n**17. Partnerships for the Goals:** Strengthening the means of implementation and revitalizing the global partnership for sustainable development.\n\nThese are our roadmap to a brighter future! Do any of these goals particularly catch your eye? 🤔 \n",
        ],
    },
]


app = Flask(__name__)


@app.route('/')
def chat():
    return render_template('base.html')

@app.route('/ask_question/', methods=['POST'])
def ask_question():
    if request.method == "POST":
        text = request.form.get("text")
        model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
                system_instruction="You are a ChatBot named TreeBo, You are like a teacher, explain everything as simple and interesting as possible, Your specialization is Sustainable Development Goals and Sustainable Development, answer only the questions related to these. If an unrelated question will ask, refused politely. You can be asked to play trivia, give user 4 options, if he chooses any option other than A,B,C,D thats wrong, and Give Message choose option A,B,C,D.",
        )

        chat_session = model.start_chat(
                history=sessionHistory
        )

        response = chat_session.send_message(text, stream=True)
            
        output = ""

        for chunk in response:
            # print(chunk.text)
            output += chunk.text

        response_data = {
            "text": output,
        }
            
        contextUser = {"role": "user", "parts": [text]}
        contextBot = {"role": "model", "parts": [output]}
        sessionHistory.append(contextUser)
        sessionHistory.append(contextBot)

        return jsonify({"data": response_data})
    else:
        return redirect(url_for('chat'))


if __name__ == '__main__':
    app.run(debug=False)