const { createApp, ref } = Vue

  const app = {
    data() {
      return {
        drawer: ref(false),
        slide: ref(1),
        searchText: ref('')
      }
    },

    methods: {
      

    },

    async created() {
      
    },

    delimiters: ['{', '}']
  }


  createApp(app).use(Quasar, { config: {} }).mount('#index')