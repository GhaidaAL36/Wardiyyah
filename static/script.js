window.addEventListener("scroll", function () {  
  // Flower 1 animation (hero section)
  const flower1 = document.getElementById("flower");
  const heroContainer = document.querySelector(".hero-container");

  if (flower1 && heroContainer) {
    const scrollY = window.scrollY; 
    const heroHeight = heroContainer.offsetHeight; 

    const scrollPercent = Math.min(scrollY / heroHeight, 1); 
    const horizontalMove = scrollPercent * 260; 
    const verticalMove = scrollPercent * 240;

    flower1.style.transform = `
      translate(calc(-60px + ${horizontalMove}px), calc(-50% + ${verticalMove}px))
    `;
    flower1.style.opacity = 1;
    flower1.style.visibility = "visible";
  }

  // Flower 2 animation (main function section)
  const flower2 = document.getElementById("flower-2");
  const section = document.querySelector("#main-function-section");

  if (flower2 && section) {
    const sectionTop = section.offsetTop;
    const scrollY = window.scrollY;
    const windowHeight = window.innerHeight;

    if (scrollY + windowHeight > sectionTop + 100) {
      const scrollPercent = Math.min(
        (scrollY + windowHeight - sectionTop) / windowHeight,
        1
      );

      const horizontalMove = scrollPercent * 60;
      const verticalMove = scrollPercent * 40;

      flower2.style.transform = `
        translateY(calc(-90% + ${verticalMove}px))
        translateX(${horizontalMove}px)
        rotate(${scrollPercent * 10}deg)
      `;

      flower2.style.opacity = 1;
      flower2.style.visibility = "visible";
    }
  }
});
/* ai */

const resultElement = document.getElementById("result");
const uploadForm = document.getElementById("upload-form");
const fileInput = document.getElementById("image-input");

// display the result
function showResult(data, uploadedImageUrl) { //takes 2 value , img user upload and data from ai
  const flowerName = data.flower;
  const description = data.description || "— لا يوجد وصف متاح حالياً —"; 

  resultElement.innerHTML = ` 
    <div class="flower-card">
      <img src="${uploadedImageUrl}" class="flower-preview" alt="صورة الزهرة" /> 

      <h2> <span class="flower-name">${flowerName}</span></h2> 
      <h2> <span class="flower-name">${data.flower_en}</span></h2> 
      <p> التصنيف: <strong>${data.label}</strong></p> 
      <p> الوصف:</p>
      <p class="flower-description">${description}</p>
      <p> الدقة: <strong>${data.confidence}%</strong></p>

      <p class="note-text"> ملاحظة: النموذج تم تدريبه على عدد محدود من صور الزهور فقط.</p>

      <button class="retry-btn" id="reset-btn"> جرب صورة جديدة</button>
    </div>
  `;


  document.getElementById("reset-btn").addEventListener("click", resetForm); 
}

function resetForm() {
  uploadForm.reset();
  resultElement.innerHTML = "";
}

// send the img to ai 
uploadForm.addEventListener("submit", async function (e) {
  e.preventDefault();

  const file = fileInput.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);
  const previewUrl = URL.createObjectURL(file);

  resultElement.innerHTML = `<p>جارٍ التعرف على الزهرة...</p>`;

  try {
    const res = await fetch("/app", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    showResult(data, previewUrl);

  } catch (error) {
    console.error("❌ فشل الاتصال:", error);
    resultElement.innerHTML = `
      <p class="error">❌ حدث خطأ أثناء الاتصال بالخادم. حاول مرة أخرى.</p>
    `;
  }
});
