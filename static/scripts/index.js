const { createApp, ref } = Vue
const { useQuasar } = Quasar

  const app = {

    setup() {
      const $q = useQuasar()
      return {
        notify(color, message, error) {
          if (error !== undefined) {
            let code=error.response.status;
            if (code === 404 || code === 409 || code === 405) message=error.response.data;
          }
          $q.notify({
            message: message,
            color: color
          })
        }
      }
    },

    data() {
      return {
        drawer: ref(false),
        slide: ref(1),
        searchText: ref(''),
        productList: ref([]),
        alert: ref(false),
        current_product_id: ref(null),
        new_name: ref(null),
        new_quantity: ref(null),
        productListClone: ref([]),
        addProductModal: ref(false),

      }
    },

    methods: {

      getAll() {
        axios.get("/getAll")
        .then(response => {
          this.productListClone = response.data;
          this.productList = response.data;
        })
        .catch(error => {
          console.log(error);
          this.notify('red', 'An error has occurred', error);
        })
      },

      addOne(id) {
        axios.post("/addOne?id=" + id)
        .then(response => {
          this.getAll();
        })
        .catch(error => {
          console.log(error);
          this.notify('red', 'An error has occurred', error);
        })
      },

      removeOne(id) {
        axios.post("/removeOne?id=" + id)
        .then(response => {
          this.getAll();
        })
        .catch(error => {
          console.log(error);
          this.notify('red', 'An error has occurred', error);
        })
      },

      deleteAll(id) {
        axios.post("/deleteAll?id=" + id)
        .then(response => {
          this.getAll();
          this.notify('primary', 'Product successfully deleted');
        })
        .catch(error => {
          console.log(error);
          this.notify('red', 'An error has occurred', error);
        })
      },

      modify() {
        axios.post("/modify?id=" + this.current_product_id + "&quantity=" + this.new_quantity + "&name=" + this.new_name)
        .then(response => {
          this.getAll();
          this.notify('primary', 'Successfully modified product');
        })
        .catch(error => {
          console.log(error);
          this.notify('red', 'An error has occurred', error);
        })
        this.alert=false;
      },

      addProduct() {
        axios.post("/add?quantity=" + this.new_quantity + "&name=" + this.new_name)
        .then(response => {
          this.getAll();
          this.notify('primary', 'Product successfully added');
        })
        .catch(error => {
          console.log(error);
          this.notify('red', 'An error has occurred', error);
        })
        this.addProductModal=false;
      }

    },

    async created() {
      await this.getAll();
    },

    watch: {
      searchText: function() {
        if (this.searchText === '') {
          this.productList = this.productListClone;
        }
        else {
          const res = this.productListClone.filter(ele => 
            ele['name'].toLowerCase().indexOf(this.searchText.toLowerCase()) > -1
          );
          this.productList = res;
        }
      }
    },
    
    delimiters: ['{', '}']
  }


  createApp(app).use(Quasar, { config: {} }).mount('#index')