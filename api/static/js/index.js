window.addEventListener("DOMContentLoaded", () => {
	const yandexService = document.getElementById("yandexService");
	const tokenInput = document.getElementById("tokenInput");
	window.YaAuthSuggest.init({
		  client_id: '5b92a3ed3922473db8837fe35791ad90',
		  response_type: 'token',
		  redirect_uri: 'http://127.0.0.1:8000/token'
	   },
	   'http://127.0.0.1:8000', 
	   {
		  view: 'button',
		  parentId: 'yandexBtn',
		  buttonView: 'main',
		  buttonTheme: 'light',
		  buttonSize: 'm',
		  buttonBorderRadius: 10
	   }
	)
	.then((result) => {
	 	yandexService.style.visibility = "visible";
	   	return result.handler();
	})
	.catch((error) => {
	   console.log('Что-то пошло не так: ', error);
	})
 
	const token = localStorage.getItem('yandex_oauth_token');
	if(token) {
		tokenInput.value = token;
	}
	const selectedItems = []
	const downloadAllBtn = document.getElementById("downloadAll")
	const contentList = document.querySelector(".content__list")
	const baseURL = `${window.location.protocol}//${window.location.host}`;
	const downloadAllUrl = new URL(baseURL + (downloadAllBtn?.getAttribute("href") || ""));


	contentList?.addEventListener("click", (event) => {
		const target = event.target;
		if(!target.classList.contains("content__list-item")) return;
		const contentPath = event.target.getAttribute("data-path");

		if(!target.classList.contains("selected")) {
			event.target.classList.add("selected");
			selectedItems.push(contentPath);
		} else {
			event.target.classList.remove("selected");
			selectedItems.splice(selectedItems.indexOf(contentPath), 1);
		}
		downloadAllUrl.searchParams.set("pathes", selectedItems.toString())
		downloadAllBtn.setAttribute("href", downloadAllUrl.toString());
	})
	
 });