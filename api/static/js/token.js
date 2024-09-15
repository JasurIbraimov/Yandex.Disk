window.addEventListener("DOMContentLoaded", () => {
    const hash = window.location.hash;
    const token = hash.match(/access_token=([^&]*)/)[1];
    const publicKey = document.getElementById("publicKey");
    localStorage.setItem("yandex_oauth_token", token);
    publicKey.addEventListener("click", (event) => {
        navigator.clipboard.writeText(token);
        if (!event.target.classList.contains("animation-done")) {
            event.target.classList.add("animation-done");
            setTimeout(
                () => event.target.classList.remove("animation-done"),
                3000
            );
        }
    });
});
