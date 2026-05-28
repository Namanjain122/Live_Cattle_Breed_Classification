# from groq import Groq
# from dotenv import load_dotenv
# import os

# load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API"))
# def ask_doctor(prompt):
#     response = client.chat.completions.create(
#         model="openai/gpt-oss-120b",
#         messages=[{
#             "role": "system", 
#              "content": """
#                 You are MR. Doctor,
#                 an expert veterinary doctor
#                 specialized in cows and buffaloes.

#                 Provide:
#                 - disease guidance
#                 - feeding advice
#                 - cattle care
#                 - vaccination suggestions
#                 - breed-related information

#                 Keep answers practical and concise.
#                 """
#         }, {
#             "role": "user",
#             "content": prompt
#         }]
#     )
#     return response.choices[0].message.content
from groq import Groq
from dotenv import load_dotenv

import os
import streamlit as st

from utils.chatbot_limit import (
    can_use_chatbot,
    increase_query_count
)

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API")
)

# =========================================
# ASK DOCTOR
# =========================================
def ask_doctor(prompt):

    user_id = st.session_state.user_id

    # =========================================
    # LIMIT CHECK
    # =========================================
    if not can_use_chatbot(user_id):

        return """
        ❌ You already used your free MR. Doctor query.
        """

    # =========================================
    # API RESPONSE
    # =========================================
    response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[

            {
                "role": "system",

                "content": """
                You are MR. Doctor,
                an expert veterinary doctor
                specialized in cows and buffaloes.

                Provide:
                - disease guidance
                - feeding advice
                - cattle care
                - vaccination suggestions
                - breed-related information

                Keep answers concise and practical.
                """
            },

            {
                "role": "user",
                "content": prompt
            }

        ]
    )

    # =========================================
    # UPDATE LIMIT
    # =========================================
    increase_query_count(user_id)

    return response.choices[0].message.content