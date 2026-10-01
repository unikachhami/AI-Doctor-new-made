const sections = [
    ["navbar", "navbar.html"],
    ["hero", "hero.html"],
    ["how-it-works", "how-it-works.html"],
    ["consultation", "consultation.html"],
    ["doctors", "doctors.html"],
    ["footer", "footer.html"]
];

async function loadSection(id, file) {
    const target = document.getElementById(id);

    if (!target) return;

    try {
        const response = await fetch("./sections/" + file);

        if (!response.ok) {
            throw new Error(
                `${file} returned ${response.status}`
            );
        }

        const html = await response.text();

        target.innerHTML = html;

    } catch (error) {

        console.error("Section error:", error);

        target.innerHTML = `
            <div style="
                padding:40px;
                text-align:center;
                color:#ff6b6b;
                font-family:Arial;
            ">
                Failed to load ${file}
            </div>
        `;
    }
}


async function initializePage() {

    for (const [id, file] of sections) {
        await loadSection(id, file);
    }

    // Smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(link => {

        link.addEventListener("click", function(event) {

            const targetId = this.getAttribute("href");
            const target = document.querySelector(targetId);

            if (!target) return;

            event.preventDefault();

            target.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        });

    });


    // Mobile menu
    const mobileMenu =
        document.getElementById("mobileMenu");

    const navLinks =
        document.querySelector(".nav-links");

    if (mobileMenu && navLinks) {

        mobileMenu.addEventListener("click", () => {
            navLinks.classList.toggle("mobile-active");
        });

    }
}


initializePage();