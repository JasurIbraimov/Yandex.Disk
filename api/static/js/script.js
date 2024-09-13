window.YaAuthSuggest.init(
    {
        client_id: "dd4c263b05d74e41bbe6047a6f1eaf4e",
        response_type: "token",
        redirect_uri: "http://127.0.0.1:8000/",
    },
    "http://127.0.0.1",
    { view: "default" }
)
    .then(({ handler }) => handler())
    .then((data) => console.log("Сообщение с токеном", data))
    .catch((error) => console.log("Обработка ошибки", error));
