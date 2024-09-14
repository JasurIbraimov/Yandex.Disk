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

 
 });