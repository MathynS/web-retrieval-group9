var url = window.location.href;
var regex = /authors\/(\d+)/;
var author_id = regex.exec(url)[1];

axios.post('/api/get-author-graph', {
	author_id: author_id
})
.then(response => console.log(response))
.catch(error => console.log(error));