const { createApp, ref } = Vue

  const app = {
    data() {
      return {
        drawer: ref(false),
        slide: ref(1),
        searchText: ref(''),
        productList: ref([]),
        alert: ref(false),
        current_product_id: ref(null),
        new_name: ref(null),
        new_quantity: ref(null)

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

      modify() {
        axios.post("/modify?id=" + this.current_product_id + "&quantity=" + this.new_quantity + "&name=" + this.new_name)
        .then(response => {
          this.getAll();
        })
        .catch(error => {
          console.log(error);
        })
        this.alert=false;
      }

    },

    async created() {
      await this.getAll();
    },

    delimiters: ['{', '}']
  }


  createApp(app).use(Quasar, { config: {} }).mount('#index')