app.component('errors', {
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
