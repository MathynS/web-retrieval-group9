<template>
    <div>
    </div>
</template>

<script>
    export default {
        data: function(){
            return{
                result: null
            }
        },
        mounted() {
            var url = window.location.href;
            var regex = /authors\/(\d+)/;
            var author_id = regex.exec(url)[1];
            axios.post('/api/get-author-fields', {
                author_id: author_id
            })
            .then(response => console.log(response))
            .catch(error => console.log(error));
        }

    }
</script>
