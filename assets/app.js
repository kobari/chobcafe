var app = new Vue({
    el: '#app',
    data: {
        items:null
    },
    mounted: function () {
        axios.get("./assets/output.json").then(response => (
            this.items = response.data
            )
        ).catch(error => console.log(error))
    }
})
