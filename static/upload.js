const uploadPanel = document.getElementById("upload-panel");
const uploadDropzone = document.getElementById("upload-dropzone");
const uploadFileInput = document.getElementById("upload-file");
const uploadFileLabel = document.getElementById("upload-file-label");
const uploadFileName = document.getElementById("upload-file-name");
const uploadSubmit = document.getElementById("upload-submit");
const uploadDownload = document.getElementById("upload-download");
const uploadReset = document.getElementById("upload-reset");
const uploadStatus = document.getElementById("upload-status");

let selectedPayload = null;
let selectedFileName = "";

function setUploadStatus(message, tone = "neutral") {
  uploadStatus.textContent = message;
  uploadStatus.className = `upload-status ${tone}`;
}

function getUploadMode() {
  const checked = uploadPanel.querySelector('input[name="upload-mode"]:checked');
  return checked ? checked.value : "replace";
}

function clearSelectedFile() {
  selectedPayload = null;
  selectedFileName = "";
  uploadFileInput.value = "";
  uploadFileLabel.classList.remove("hidden");
  uploadFileName.classList.add("hidden");
  uploadFileName.textContent = "";
  uploadSubmit.disabled = true;
  uploadDropzone.classList.remove("has-file");
}

function setSelectedFile(name, payload) {
  selectedPayload = payload;
  selectedFileName = name;
  uploadFileLabel.classList.add("hidden");
  uploadFileName.classList.remove("hidden");
  uploadFileName.textContent = name;
  uploadSubmit.disabled = false;
  uploadDropzone.classList.add("has-file");
}

function parseJsonFile(text, fileName) {
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    throw new Error("Geçersiz JSON dosyası");
  }

  if (!data || typeof data !== "object" || Array.isArray(data)) {
    throw new Error("Kök öğe bir JSON nesnesi olmalı");
  }

  if (!data.categories || typeof data.categories !== "object") {
    throw new Error("Dosyada 'categories' alanı zorunlu");
  }

  return {
    mode: getUploadMode(),
    categories: data.categories,
  };
}

function handleFile(file) {
  if (!file) return;

  if (!file.name.toLowerCase().endsWith(".json") && file.type !== "application/json") {
    setUploadStatus("Lütfen yalnızca .json dosyası seçin", "error");
    return;
  }

  const reader = new FileReader();
  reader.onload = () => {
    try {
      const payload = parseJsonFile(reader.result, file.name);
      setSelectedFile(file.name, payload);
      setUploadStatus(`"${file.name}" hazır — Yükle'ye basın`, "neutral");
    } catch (error) {
      clearSelectedFile();
      setUploadStatus(error.message, "error");
    }
  };
  reader.onerror = () => {
    setUploadStatus("Dosya okunamadı", "error");
  };
  reader.readAsText(file, "UTF-8");
}

uploadDropzone.addEventListener("click", () => uploadFileInput.click());

uploadDropzone.addEventListener("keydown", (event) => {
  if (event.key === "Enter" || event.key === " ") {
    event.preventDefault();
    uploadFileInput.click();
  }
});

uploadFileInput.addEventListener("change", () => {
  const [file] = uploadFileInput.files;
  handleFile(file);
});

uploadDropzone.addEventListener("dragover", (event) => {
  event.preventDefault();
  uploadDropzone.classList.add("dragover");
});

uploadDropzone.addEventListener("dragleave", () => {
  uploadDropzone.classList.remove("dragover");
});

uploadDropzone.addEventListener("drop", (event) => {
  event.preventDefault();
  uploadDropzone.classList.remove("dragover");
  const [file] = event.dataTransfer.files;
  handleFile(file);
});

uploadPanel.querySelectorAll('input[name="upload-mode"]').forEach((input) => {
  input.addEventListener("change", () => {
    if (selectedPayload) {
      selectedPayload.mode = getUploadMode();
    }
  });
});

async function uploadQuestions() {
  if (!selectedPayload) return;

  selectedPayload.mode = getUploadMode();
  uploadSubmit.disabled = true;
  setUploadStatus("Yükleniyor…", "neutral");

  try {
    const response = await fetch("/api/questions/upload", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(selectedPayload),
    });

    const body = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(body.detail || "Yükleme başarısız");
    }

    const names = (body.categories || []).join(", ");
    setUploadStatus(
      `Yüklendi (${body.mode}): ${body.category_count} kategori — ${names}`,
      "success"
    );
    clearSelectedFile();
  } catch (error) {
    setUploadStatus(error.message, "error");
    uploadSubmit.disabled = Boolean(selectedPayload);
  }
}

async function downloadCurrentBank() {
  setUploadStatus("İndiriliyor…", "neutral");
  try {
    const response = await fetch("/api/questions");
    if (!response.ok) {
      const body = await response.json().catch(() => ({}));
      throw new Error(body.detail || "İndirme başarısız");
    }
    const data = await response.json();
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: "application/json;charset=utf-8",
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "questions.json";
    link.click();
    URL.revokeObjectURL(url);
    setUploadStatus("Mevcut soru bankası indirildi", "success");
  } catch (error) {
    setUploadStatus(error.message, "error");
  }
}

async function resetQuestionBank() {
  if (
    !window.confirm(
      "Varsayılan gömülü soru bankasına dönülsün mü? Yüklediğiniz özel sorular silinir."
    )
  ) {
    return;
  }

  uploadReset.disabled = true;
  setUploadStatus("Sıfırlanıyor…", "neutral");

  try {
    const response = await fetch("/api/questions/reset", { method: "POST" });
    const body = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(body.detail || "Sıfırlama başarısız");
    }

    setUploadStatus(body.message || "Varsayılan banka yüklendi", "success");
    clearSelectedFile();
  } catch (error) {
    setUploadStatus(error.message, "error");
  } finally {
    uploadReset.disabled = false;
  }
}

uploadSubmit.addEventListener("click", uploadQuestions);
uploadDownload.addEventListener("click", downloadCurrentBank);
uploadReset.addEventListener("click", resetQuestionBank);
