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
        addProductModal: ref(false)

      }
    },

    methods: {

      get_all_product() {
        axios.get("/product")
        .then(response => {
          this.productListClone = response.data;
          this.productList = response.data;
        })
        .catch(error => {
          console.log(error);
          this.notify('red', 'An error has occurred', error);
        })
      },

      add_product() {
        const product = {'name':this.new_name, 'quantity':this.new_quantity}
        axios.post("/product", product)
        .then(response => {
          this.get_all_product();
          this.notify('primary', 'Product successfully added');
        })
        .catch(error => {
          console.log(error);
          this.notify('red', 'An error has occurred', error);
        })
        .finally(() => this.addProductModal=false);
      },

      delete_product(id) {
        axios.delete("/product/" + id)
        .then(response => {
          this.get_all_product();
          this.notify('primary', 'Product successfully deleted');
        })
        .catch(error => {
          console.log(error);
          this.notify('red', 'An error has occurred', error);
        })
      },

      modify_product(id) {
        const product = {'name':this.new_name, 'quantity':this.new_quantity}
        axios.put("/product/" + id, product)
        .then(response => {
          this.get_all_product();
          this.notify('primary', 'Successfully modified product');
        })
        .catch(error => {
          console.log(error);
          this.notify('red', 'An error has occurred', error);
        })
        this.alert=false;
      },

       modify_product_quantity(el, quantity) {
        console.log(el)
        const product = {'name':el.name, 'quantity':el.quantity + quantity}

         if (product.quantity <= 0)
          return this.delete_product(el.id)

        axios.put("/product/" + el.id, product)
        .then(response => {
          this.get_all_product();
          this.notify('primary', 'Successfully modified product');
        })
        .catch(error => {
          console.log(error);
          this.notify('red', 'An error has occurred', error);
        })
        this.alert=false;
      },

    },

    async created() {
      await this.get_all_product();
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