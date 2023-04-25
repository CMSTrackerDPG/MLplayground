const app_discover = Vue.createApp({
    data() {
        return {
            file_discover_is_visible: false,
            api_base: '/api/histogram_data_files/',
            page_current_url:
                '/api/histogram_data_files/' + window.location.search,
            abort_controller: new AbortController(), // To cancel a request
        };
    },
    // This will run as soon as the app is mounted
    methods: {
        // Private method to fetch updated files information
        // via the API
        show_file_discover_modal() {
            this.file_discover_is_visible = true;
        },
        hide_file_discover_modal() {
            this.file_discover_is_visible = false;
        },
    },
    computed: {
        request_url() {
            // window.location.search contains the filters
            // selected by the user in the filter form
            return this.page_current_url;
        },
    },
});
