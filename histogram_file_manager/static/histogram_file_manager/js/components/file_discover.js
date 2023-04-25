app_discover.component('file-discover', {
    // delimiters: ['{', '}'],
    template:
        /*html*/
        `
<!-- :class="{ hidden: !is_visible }" -->
<div id="modal-file-discover" class="modal modal-extra" :class="{ shown: is_visible }" tabindex="-1" role="dialog">
  <div class="modal-dialog" role="document">
	<div class="modal-content">
	  <div class="modal-header">
        <h5 class="modal-title">Discover files</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" v-on:click="clicked_close"></button>
	  </div>
	  <div class="modal-body">
    <success :success="success" @dismissed-success="dismiss_success"></success>
	<errors :errors="errors" @dismissed-error="dismiss_error"></errors>
    <div class="d-grid" style="padding: 8px">
      Click the button below to start discovering files on EOS.
      <button @click="discover_files()"
          class="btn btn-primary" style="margin-top: 5pt">
        Discover files
      </button>
    </div>
      </div>
      <div class="modal-footer">
      </div>
    </div>
  </div>
</div>
		`,
    data() {
        return {
            errors: [],
            success: [],
            message_id: 0,
        };
    },
    props: {
        is_visible: {
            type: Boolean,
            required: true,
        }
    },
    methods: {
        clicked_close() {
            console.debug('Modal was closed');
            this.errors = [];
            this.success = [];
            this.message_id = 0;
            this.$emit('clicked-close');
        },
        // Callback for discovering files 
        discover_files() {
            console.debug('Initialising file discovery');
            data = {};
            console.debug('Sending the following data wtih GET request:');
            console.debug(data);
            console.debug(get_axios_config());
            axios.get(
                `/api/histogram_data_files/discover/`, data, get_axios_config(),
            )
            .then((response) => {
                console.log(response);
                this.success.push({
                    id: this.message_id,
                    message: `File discovery initialised.`
                });
                this.message_id += 1;
            })
            .catch((error) => {
                console.error(error);
                this.errors.push({
                    id: this.message_id,
                    message: `${error}: ${error.response.data}`
                });
                this.message_id += 1;
            });
        },
        // Callback for error dismissal from errors component
        dismiss_error(error) {
            console.debug(`this.errors is ${this.errors}`)
            console.debug(`Dismissing error alert with ID ${error.id}`);
            for (var i = 0; i < this.errors.length; i++) {
                if (this.errors[i].id === error.id) {
                  this.errors.splice(i, 1);
                  i -= 1;
                }
            }
            console.debug(`Now this.errors is ${this.errors}`)
        },
        dismiss_success(s) {
          console.debug(`Dismissing success alert with ID ${s.id}`);
          for (var i = 0; i < this.success.length; i++) {
              if (this.success[i].id === s.id) {
                  this.success.splice(i, 1);
                  i -= 1;
              }
          }
        },
    },
});

app_discover.component('errors', {
    template:
        /*html*/
        `
<div v-show="has_errors">
  <div 
	role="alert"
	class="alert alert-danger alert-dismissable fade show"
	v-for="error in errors">
    <div class="row">
      <div class="col-1">
        <button
        type="button"
        class="btn-close"
        data-bs-dismiss="alert"
        aria-label="Close">
        </button>
      </div>
      <div class="col-11">
        {{ error.message }}
      </div>
    </div>

  </div>
</div>
		`,
    props: {
        errors: {
            type: Array,
            required: true,
        },
    },
    computed: {
        has_errors() {
            return this.errors.length > 0;
        },
    },
    methods: {
        dismiss_error(error) {
            this.$emit('dismissed-error', error);
        },
    },
});

app_discover.component('success', {
    template:
        /*html*/
        `
<div v-show="has_success">
  <div 
	role="alert"
	class="alert alert-success alert-dismissable fade show"
	v-for="s in success">
    <div class="row">
      <div class="col-1">
        <button
        type="button"
        class="btn-close"
        data-bs-dismiss="alert"
        aria-label="Close">
        </button>
      </div>
      <div class="col-11">
        {{ s.message }}
      </div>
    </div>

  </div>
</div>
		`,
    props: {
        success: {
            type: Array,
            required: true,
        },
    },
    computed: {
        has_success() {
            return this.success.length > 0;
        },
    },
    methods: {
        dismiss_success(success) {
            this.$emit('dismissed-success', success);
        },
    },
});
