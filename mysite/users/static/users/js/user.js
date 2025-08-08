function copyToClipboard() {
    const input = document.getElementById("profileUrl");
    input.select();
    input.setSelectionRange(0, 99999); // mobile support
    document.execCommand("copy");
    alert("網址已複製到剪貼簿");
}