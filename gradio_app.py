import os
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv

from brain_of_the_doctor import (
    encoded_image,
    analyze_image_with_querry
)

from voice_of_user import (
    transcribe_using_groq
)

from voice_of_ai import (
    text_to_speech_elevenlabs
)


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"
SECTIONS_DIR = FRONTEND_DIR / "sections"
CSS_DIR = FRONTEND_DIR / "css"


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# ============================================================
# AI MODELS
# ============================================================

STT_MODEL = "whisper-large-v3"
VISION_MODEL = "qwen/qwen3.8-27b"


# ============================================================
# FIND FRONTEND FILE
# ============================================================

def find_frontend_file(filename):

    # First check:
    # frontend/sections/filename

    direct_path = SECTIONS_DIR / filename

    if direct_path.exists():
        print(f"Loading: {direct_path}")
        return direct_path


    # Search entire frontend directory

    if FRONTEND_DIR.exists():

        matches = list(
            FRONTEND_DIR.rglob(filename)
        )

        if matches:

            print(f"Found: {matches[0]}")

            return matches[0]


    return None


# ============================================================
# LOAD HTML
# ============================================================

def load_html(filename):

    path = find_frontend_file(filename)

    if path is None:

        print(
            f"WARNING: Missing frontend file: {filename}"
        )

        return ""

    try:

        return path.read_text(
            encoding="utf-8"
        )

    except Exception as e:

        print(
            f"ERROR loading {filename}: {e}"
        )

        return ""


# ============================================================
# LOAD CSS
# ============================================================

def load_css():

    css_files = [

        "style.css",
        "navbar.css",
        "hero.css",
        "sections.css",
        "consultation.css",
        "doctors.css",
        "footer.css",
        "responsive.css"

    ]

    final_css = ""

    for filename in css_files:

        path = CSS_DIR / filename

        if path.exists():

            print(
                f"Loading CSS: {path}"
            )

            try:

                final_css += "\n\n"

                final_css += path.read_text(
                    encoding="utf-8"
                )

            except Exception as e:

                print(
                    f"ERROR loading CSS {filename}: {e}"
                )

        else:

            print(
                f"WARNING: Missing CSS: {path}"
            )

    return final_css


# ============================================================
# AI PROCESSING
# ============================================================

def process_inputs(
    audio_file_path,
    image_file_path
):

    try:

        # ----------------------------------------------------
        # AUDIO CHECK
        # ----------------------------------------------------

        if audio_file_path is None:

            return (
                "",
                "Please speak your symptoms.",
                None
            )


        # ----------------------------------------------------
        # IMAGE CHECK
        # ----------------------------------------------------

        if image_file_path is None:

            return (
                "",
                "Please capture or upload a medical image.",
                None
            )


        # ----------------------------------------------------
        # SPEECH TO TEXT
        # ----------------------------------------------------

        speech_to_text_output = transcribe_using_groq(

            stt_model=STT_MODEL,

            audio_file_path=audio_file_path,

            GROQ_API_KEY=GROQ_API_KEY

        )


        print()
        print("================================")
        print("PATIENT")
        print("================================")
        print(speech_to_text_output)


        # ----------------------------------------------------
        # ENCODE IMAGE
        # ----------------------------------------------------

        image_base64 = encoded_image(
            image_file_path
        )


        # ----------------------------------------------------
        # AI DOCTOR
        # ----------------------------------------------------

        doctor_response = analyze_image_with_querry(

            query=speech_to_text_output,

            encoded_image=image_base64,

            image_path=image_file_path,

            model=VISION_MODEL

        )


        print()
        print("================================")
        print("ALPHA AI DOCTOR")
        print("================================")
        print(doctor_response)


        # ----------------------------------------------------
        # TEXT TO SPEECH
        # ----------------------------------------------------

        voice_of_doctor = text_to_speech_elevenlabs(

            input_text=doctor_response,

            output_filepath=str(
                BASE_DIR / "final.mp3"
            )

        )


        # ----------------------------------------------------
        # RETURN
        # ----------------------------------------------------

        return (

            speech_to_text_output,

            doctor_response,

            voice_of_doctor

        )


    except Exception as e:

        print()
        print("================================")
        print("ERROR")
        print("================================")
        print(e)

        return (

            "",

            f"Error: {str(e)}",

            None

        )


# ============================================================
# CSS
# ============================================================

CUSTOM_CSS = load_css()


# ============================================================
# GRADIO APP
# ============================================================

with gr.Blocks(
    title="ALPHA | AI Health Assistant"
) as demo:


    # ========================================================
    # NAVBAR
    # ========================================================

    navbar_html = load_html(
        "navbar.html"
    )

    if navbar_html:

        gr.HTML(
            navbar_html
        )


    # ========================================================
    # HERO
    # ========================================================

    hero_html = load_html(
        "hero.html"
    )

    if hero_html:

        gr.HTML(
            hero_html
        )


    # ========================================================
    # STATS
    # ========================================================

    gr.HTML(
        """
        <section class="stats-section">

            <div class="stats-container">

                <div class="stat">

                    <strong>24/7</strong>

                    <span>
                        AI Availability
                    </span>

                </div>


                <div class="stat-divider"></div>


                <div class="stat">

                    <strong>Voice</strong>

                    <span>
                        Interaction
                    </span>

                </div>


                <div class="stat-divider"></div>


                <div class="stat">

                    <strong>Vision</strong>

                    <span>
                        Image Analysis
                    </span>

                </div>


                <div class="stat-divider"></div>


                <div class="stat">

                    <strong>AI</strong>

                    <span>
                        Health Assessment
                    </span>

                </div>

            </div>

        </section>
        """
    )


    # ========================================================
    # HOW IT WORKS
    # ========================================================

    how_html = load_html(
        "how-it-works.html"
    )

    if how_html:

        gr.HTML(
            how_html
        )


    # ========================================================
    # AI CONSULTATION HEADER
    # ========================================================

    gr.HTML(
        """
        <section
            id="consultation"
            class="consultation-section"
        >

            <div class="consultation-container">

                <div class="consultation-heading">

                    <div class="section-label">
                        AI Consultation
                    </div>

                    <h2>
                        Talk to
                        <span>Alpha.</span>
                    </h2>

                    <p>
                        Describe your symptoms, share a
                        medical image, and receive an
                        AI-generated health assessment.
                    </p>

                </div>

            </div>

        </section>
        """
    )


    # ========================================================
    # INPUT SECTION
    # ========================================================

    with gr.Row(
        elem_classes="consultation-interface"
    ):


        # ====================================================
        # VOICE CARD
        # ====================================================

        with gr.Column(
            elem_classes="input-card"
        ):

            gr.HTML(
                """
                <div class="input-card-header">

                    <div class="input-icon">
                        🎙
                    </div>

                    <div>

                        <h3>
                            Voice Consultation
                        </h3>

                        <p>
                            Tell Alpha what you
                            are experiencing.
                        </p>

                    </div>

                </div>
                """
            )


            audio_input = gr.Audio(

                sources=[
                    "microphone"
                ],

                type="filepath",

                label="Record your symptoms",

                elem_classes="alpha-audio"

            )


        # ====================================================
        # IMAGE CARD
        # ====================================================

        with gr.Column(
            elem_classes="input-card"
        ):

            gr.HTML(
                """
                <div class="input-card-header">

                    <div class="input-icon">
                        ⌁
                    </div>

                    <div>

                        <h3>
                            Medical Image
                        </h3>

                        <p>
                            Upload or capture an
                            image for analysis.
                        </p>

                    </div>

                </div>
                """
            )


            image_input = gr.Image(

                sources=[
                    "upload",
                    "webcam"
                ],

                type="filepath",

                label="Upload / Capture Image",

                elem_classes="alpha-image"

            )


    # ========================================================
    # ANALYZE BUTTON
    # ========================================================

    with gr.Row(
        elem_classes="analyze-wrapper"
    ):

        analyze_button = gr.Button(

            "Analyze with Alpha →",

            variant="primary",

            elem_classes="alpha-analyze-button"

        )


    # ========================================================
    # ASSESSMENT CARD
    # ========================================================

    with gr.Column(
        elem_classes="assessment-card"
    ):


        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        gr.HTML(
            """
            <div class="assessment-header">

                <div>

                    <div class="assessment-label">
                        ALPHA ASSESSMENT
                    </div>

                    <h3>
                        AI Health Response
                    </h3>

                </div>


                <div class="assessment-status">

                    <span></span>

                    READY

                </div>

            </div>
            """
        )


        # ----------------------------------------------------
        # PATIENT SYMPTOMS
        # ----------------------------------------------------

        speech_output = gr.Textbox(

            label="Patient Symptoms",

            interactive=False,

            lines=3,

            elem_classes="patient-output"

        )


        # ----------------------------------------------------
        # AI RESPONSE
        # ----------------------------------------------------

        doctor_output = gr.Markdown(

            value="""
Your AI assessment will appear here.
""",

            elem_classes="doctor-output"

        )


        # ----------------------------------------------------
        # VOICE RESPONSE
        # ----------------------------------------------------

        gr.HTML(
            """
            <div class="voice-response">

                <div class="voice-response-icon">
                    ◖
                </div>

                <div>

                    <strong>
                        Alpha Voice Response
                    </strong>

                    <span>
                        AI generated audio response
                    </span>

                </div>

            </div>
            """
        )


        audio_output = gr.Audio(

            label="Alpha Voice",

            autoplay=True,

            elem_classes="alpha-output-audio"

        )


    # ========================================================
    # BUTTON CONNECTION
    # ========================================================

    analyze_button.click(

        fn=process_inputs,

        inputs=[
            audio_input,
            image_input
        ],

        outputs=[
            speech_output,
            doctor_output,
            audio_output
        ]

    )


    # ========================================================
    # HUMAN DOCTOR SECTION
    # ========================================================
    #
    # IMPORTANT:
    # No doctors.html required.
    # This section is directly inside this Python file.
    #

    gr.HTML(
        """
        <section
            id="doctors"
            class="doctors-section"
        >

            <div class="doctors-container">

                <div class="doctor-cta">


                    <div class="doctor-cta-content">

                        <div class="section-label">
                            Human Care
                        </div>


                        <h2>
                            Need a human doctor?
                        </h2>


                        <p>
                            Alpha can help you understand
                            your symptoms. When you want
                            professional human care,
                            connect with a qualified
                            doctor or clinic.
                        </p>


                        <div class="doctor-actions">

                            <a
                                href="tel:+9770000000000"
                                class="primary-button"
                            >
                                Call Doctor
                            </a>


                            <a
                                href="mailto:doctor@example.com"
                                class="secondary-button"
                            >
                                Email Doctor
                            </a>

                        </div>

                    </div>


                    <div class="doctor-visual">

                        <div
                            class="doctor-orbit orbit-a"
                        ></div>


                        <div
                            class="doctor-orbit orbit-b"
                        ></div>


                        <div class="medical-circle">

                            <div class="medical-cross">
                                +
                            </div>

                        </div>

                    </div>

                </div>

            </div>

        </section>
        """
    )


    # ========================================================
    # FOOTER
    # ========================================================

    footer_html = load_html(
        "footer.html"
    )

    if footer_html:

        gr.HTML(
            footer_html
        )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    print()
    print("========================================")
    print("        ALPHA AI DOCTOR")
    print("========================================")
    print()
    print(f"Project: {BASE_DIR}")
    print(f"Frontend: {FRONTEND_DIR}")
    print()
    print("Starting Gradio...")
    print()
    print("Open:")
    print("http://127.0.0.1:7861")
    print()

    demo.launch(

        server_name="127.0.0.1",

        server_port=7861,

        inbrowser=True,

        css=CUSTOM_CSS

    )