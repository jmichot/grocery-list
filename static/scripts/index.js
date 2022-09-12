const { createApp, ref } = Vue

  const app = {
    data() {
      return {
        drawer: ref(false),
        slide: ref(1),
        searchText: ref(''),
        productList: ref([])
      }
    },

    methods: {
      
      getAll() {
        axios.get("/getAll")
        .then(response => {
          this.productList = response.data;
        })
        .catch(error => {
          console.log(error);
        })
      },

      addOne(id) {
        axios.post("/addOne?id=" + id)
        .then(response => {
          this.getAll();
        })
        .catch(error => {
          console.log(error);
        })
      },

      removeOne(id) {
        axios.post("/removeOne?id=" + id)
        .then(response => {
          this.getAll();
        })
        .catch(error => {
          console.log(error);
        })
      },

      deleteAll(id) {
        axios.post("/deleteAll?id=" + id)
        .then(response => {
          this.getAll();
        })
        .catch(error => {
          console.log(error);
        })
      },

      modify(id) {

      }

    },

    async created() {
      await this.getAll();
    },

    delimiters: ['{', '}']
  }


  createApp(app).use(Quasar, { config: {} }).mount('#index')