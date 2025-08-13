function copyToClipboard() {
    const input = document.getElementById("profileUrl");
    input.select();
    input.setSelectionRange(0, 99999); // mobile support
    document.execCommand("copy");
    alert("網址已複製到剪貼簿");
}
/**
 * 從 API 抓資料
 * @param {string} url API endpoint
 * @returns {Promise<Object>} API 回傳的 JSON 資料
 */
async function fetchData(url) {
    try {
        const response = await axios.get(url);
        return response.data;
    } catch (error) {
        console.error("資料抓取失敗:", error);
        throw error;
    }
}
