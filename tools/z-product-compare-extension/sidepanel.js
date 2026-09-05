const REVIEW_ORIGIN = "http://127.0.0.1:8765";
const frame = document.querySelector("#review");
const connection = document.querySelector("#connection");
const connectionMessage = document.querySelector("#connectionMessage");
const retry = document.querySelector("#retry");
const language = navigator.language.startsWith("ja") ? "ja" : "en";
const messages = {
  ja: {
    connection: "ローカルサーバーに接続できませんでした。次のコマンドを実行してから、再試行してください。",
    retry: "再試行"
  },
  en: {
    connection: "Could not connect to the local server. Run this command, then retry.",
    retry: "Retry"
  }
};

document.documentElement.lang = language;
connectionMessage.textContent = messages[language].connection;
retry.textContent = messages[language].retry;

const showReview = () => {
  connection.hidden = true;
  frame.hidden = false;
};

const connect = () => {
  connection.hidden = false;
  frame.hidden = true;
  frame.src = `${REVIEW_ORIGIN}/?sidepanel=1&retry=${Date.now()}`;
};

const sendResult = (ok, message = "") => {
  frame.contentWindow?.postMessage(
    { type: "zproduct:navigate-result", ok, message },
    REVIEW_ORIGIN
  );
};

const navigateActiveTab = async (value) => {
  try {
    const url = new URL(value);
    if (!["http:", "https:"].includes(url.protocol)) throw new Error("unsupportedUrl");
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab?.id) throw new Error("activeTabNotFound");
    await chrome.tabs.update(tab.id, { url: url.href });
    sendResult(true);
  } catch (error) {
    sendResult(false, error instanceof Error ? error.message : String(error));
  }
};

window.addEventListener("message", (event) => {
  if (event.origin !== REVIEW_ORIGIN || event.source !== frame.contentWindow) return;
  if (event.data?.type === "zproduct:loaded") showReview();
  if (event.data?.type === "zproduct:navigate") navigateActiveTab(event.data.url);
});

retry.addEventListener("click", () => {
  connect();
});

connect();
