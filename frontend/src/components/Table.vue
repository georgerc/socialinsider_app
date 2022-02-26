<template>
 <div>
      <date-picker v-model="time3" @change="updateRows" value-type="timestamp" range></date-picker>
    <b-table striped hover :items="items"></b-table>

    
  </div>
  
</template>

<script>
   import DatePicker from 'vue2-datepicker';
    import 'vue2-datepicker/index.css';
    import axios from "axios";

export default {
    setup() {
        name:'Table'
    },components: { DatePicker },
    methods:{
        updateRows(){
            console.log(this.time3[0])
            console.log(this.time3[1])

            axios({
   method: 'post',
  url: "http://127.0.0.1:5000/get_brands",
  headers: axios.defaults.headers.common, 
  data: {
    start_date:this.time3[0],
    end_date:this.time3[1] // This is the body part
  }
}).then(resp=>{console.log(resp.data)
  this.items=resp.data

});


        }

    },

       data() {
      return {
           time1: null,
        time2: null,
        time3: null,
        items: []
      }
    }
}
</script>
