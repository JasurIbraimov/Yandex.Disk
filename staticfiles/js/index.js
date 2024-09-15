window.addEventListener("DOMContentLoaded", () => {
    const yandexService = document.getElementById("yandexService");
    const tokenInput = document.getElementById("tokenInput");
    const yandexServiceLoader = document.getElementById("yandexLoader");
    yandexServiceLoader.style.visibility = "visible";
    window.YaAuthSuggest.init(
        {
            client_id: "5b92a3ed3922473db8837fe35791ad90",
            response_type: "token",
            redirect_uri: "http://127.0.0.1:8000/token",
        },
        "http://127.0.0.1:8000",
        {
            view: "button",
            parentId: "yandexBtn",
            buttonView: "main",
            buttonTheme: "light",
            buttonSize: "m",
            buttonBorderRadius: 10,
        }
    )
        .then((result) => {
            yandexServiceLoader.style.visibility = "hidden";
            yandexService.style.visibility = "visible";
            return result.handler();
        })
        .catch((error) => {
            console.log("Что-то пошло не так: ", error);
        });

    const token = localStorage.getItem("yandex_oauth_token");
    if (token) {
        tokenInput.value = token;
    }
    const selectedItems = [];
    const downloadAllBtn = document.getElementById("downloadAll");
    const downloadAllBtnTextElement =
        downloadAllBtn.querySelector("#downloadAllText");
    const contentListItems = document.querySelectorAll(".content__list-item");
    const baseURL = `${window.location.protocol}//${window.location.host}`;
    const downloadAllUrl = new URL(
        baseURL + (downloadAllBtn?.getAttribute("href") || "")
    );

    contentListItems.forEach((item) => {
        item.addEventListener("click", (event) => {
            const target = event.currentTarget;
            const contentPath = target.getAttribute("data-path");

            if (!target.classList.contains("selected")) {
                target.classList.add("selected");
                selectedItems.push(contentPath);
            } else {
                target.classList.remove("selected");
                selectedItems.splice(selectedItems.indexOf(contentPath), 1);
            }
            downloadAllUrl.searchParams.set("pathes", selectedItems.toString());
            downloadAllBtn.setAttribute("href", downloadAllUrl.toString());
            let downloadAllTextContent = `Скачать все выбранные (${selectedItems.length})`;
            if (selectedItems.length == 0) {
                downloadAllTextContent = "Скачать все выбранные";
            }
            downloadAllBtnTextElement.textContent = downloadAllTextContent;
        });
    });
});
