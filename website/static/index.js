function delLog(logId) {
    fetch("/wlog/deleteLog", {
        method: "POST",
        body: JSON.stringify({ logId: logId }),
    }).then((_res) => {
        // Reload the window with GET method
        window.location.href = "/wlog/myWorkLog";
    });
}
