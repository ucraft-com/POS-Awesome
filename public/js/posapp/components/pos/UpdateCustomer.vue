<template>
  <v-row justify="center">
    <v-dialog v-model="customerDialog" max-width="600px" @click:outside="clear_customer">
      <v-card>
        <v-card-title>
          <span v-if="customer_id" class="text-h5 text-primary">{{
            __('Update Customer')
          }}</span>
          <span v-else class="text-h5 text-primary">{{
            __('Create Customer')
          }}</span>
        </v-card-title>
        <v-card-text class="pa-0">
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field density="compact" color="primary" :label="frappe._('Customer Name') + ' *'"
                  bg-color="white" hide-details v-model="customer_name"></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field density="compact" color="primary" :label="frappe._('Tax ID')" bg-color="white"
                  hide-details v-model="tax_id"></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field density="compact" color="primary" :label="frappe._('Mobile No')" bg-color="white"
                  hide-details v-model="mobile_no"></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field density="compact" color="primary" :label="frappe._('Email Id')" bg-color="white"
                  hide-details v-model="email_id"></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-select density="compact" label="Gender" :items="genders" v-model="gender"></v-select>
              </v-col>
              <v-col cols="6">
                <v-text-field density="compact" color="primary" :label="frappe._('Referral Code')" bg-color="white"
                  hide-details v-model="referral_code"></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-menu ref="birthday_menu" v-model="birthday_menu" :close-on-content-click="false"
                  transition="scale-transition" density="default">
                  <template v-slot:activator="{ props }">
                    <v-text-field v-model="birthday" :label="frappe._('Birthday')" readonly density="compact" clearable
                      hide-details v-bind="props" color="primary"></v-text-field>
                  </template>
                  <v-date-picker v-model="birthday" color="primary" no-title scrollable
                    :max="frappe.datetime.now_date()" @input="birthday_menu = false">
                  </v-date-picker>
                </v-menu>
              </v-col>
              <v-col cols="6">
                <v-autocomplete clearable density="compact" auto-select-first color="primary"
                  :label="frappe._('Customer Group') + ' *'" v-model="group" :items="groups" bg-color="white"
                  :no-data-text="__('Group not found')" hide-details required>
                </v-autocomplete>
              </v-col>
              <v-col cols="6">
                <v-autocomplete clearable density="compact" auto-select-first color="primary"
                  :label="frappe._('Territory') + ' *'" v-model="territory" :items="territorys" bg-color="white"
                  :no-data-text="__('Territory not found')" hide-details required>
                </v-autocomplete>
              </v-col>
              <v-col cols="6" v-if="loyalty_program">
                <v-text-field v-model="loyalty_program" :label="frappe._('Loyalty Program')" density="compact" readonly
                  hide-details></v-text-field>
              </v-col>
              <v-col cols="6" v-if="loyalty_points">
                <v-text-field v-model="loyalty_points" :label="frappe._('Loyalty Points')" density="compact" readonly
                  hide-details></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" theme="dark" @click="close_dialog">{{
            __('Close')
          }}</v-btn>
          <v-btn color="success" theme="dark" @click="submit_dialog">{{
            __('Submit')
          }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>

export default {
  data: () => ({
    customerDialog: false,
    pos_profile: '',
    customer_id: '',
    customer_name: '',
    tax_id: '',
    mobile_no: '',
    email_id: '',
    referral_code: '',
    birthday: new Date(),
    birthday_menu: false,
    group: '',
    groups: [],
    territory: '',
    territorys: [],
    genders: [],
    customer_type: 'Individual',
    gender: '',
    loyalty_points: null,
    loyalty_program: null,
  }),
  watch: {},
  methods: {
    close_dialog() {
      this.customerDialog = false;
      this.clear_customer();
    },
    clear_customer() {
      this.customer_name = '';
      this.tax_id = '';
      this.mobile_no = '';
      this.email_id = '';
      this.referral_code = '';
      this.birthday = '';
      this.group = frappe.defaults.get_user_default('Customer Group');
      this.territory = frappe.defaults.get_user_default('Territory');
      this.customer_id = '';
      this.customer_type = 'Individual';
      this.gender = '';
      this.loyalty_points = null;
      this.loyalty_program = null;
    },
    getCustomerGroups() {
      if (this.groups.length > 0) return;
      const vm = this;
      frappe.db
        .get_list('Customer Group', {
          fields: ['name'],
          filters: { is_group: 0 },
          limit: 1000,
          order_by: 'name',
        })
        .then((data) => {
          if (data.length > 0) {
            data.forEach((el) => {
              vm.groups.push(el.name);
            });
          }
        });
    },
    getCustomerTerritorys() {
      if (this.territorys.length > 0) return;
      const vm = this;
      frappe.db
        .get_list('Territory', {
          fields: ['name'],
          filters: { is_group: 0 },
          limit: 5000,
          order_by: 'name',
        })
        .then((data) => {
          if (data.length > 0) {
            data.forEach((el) => {
              vm.territorys.push(el.name);
            });
          }
        });
    },
    getGenders() {
      const vm = this;
      frappe.db
        .get_list('Gender', {
          fields: ['name'],
          page_length: 10,
        })
        .then((data) => {
          if (data.length > 0) {
            data.forEach((el) => {
              vm.genders.push(el.name);
            });
          }
        });
    },
    submit_dialog() {
      // validate if all required fields are filled
      if (!this.customer_name) {
        this.eventBus.emit('show_message', {
          title: __('Customer name is required.'),
          color: 'error',
        });
        return;
      }
      if (!this.group) {
        this.eventBus.emit('show_message', {
          title: __('Customer group is required.'),
          color: 'error',
        });
        return;
      }
      if (!this.territory) {
        this.eventBus.emit('show_message', {
          title: __('Customer territory is required.'),
          color: 'error',
        });
        return;
      }
      if (this.customer_name) {
        var vm = this;
        const args = {
          customer_id: this.customer_id,
          customer_name: this.customer_name,
          company: this.pos_profile.company,
          tax_id: this.tax_id,
          mobile_no: this.mobile_no,
          email_id: this.email_id,
          referral_code: this.referral_code,
          birthday: frappe.format(this.birthday, { fieldtype: 'Date' }),
          customer_group: this.group,
          territory: this.territory,
          customer_type: this.customer_type,
          gender: this.gender,
          method: this.customer_id ? 'update' : 'create',
          pos_profile_doc: this.pos_profile,
        };
        frappe.call({
          method: 'posawesome.posawesome.api.posapp.create_customer',
          args: args,
          callback: (r) => {
            if (!r.exc && r.message.name) {
              let text = __('Customer created successfully.');
              if (vm.customer_id) {
                text = __('Customer updated successfully.');
              }
              vm.eventBus.emit('show_message', {
                text: text,
                color: 'success',
              });
              args.name = r.message.name;
              frappe.utils.play_sound('submit');
              vm.eventBus.emit('add_customer_to_list', args);
              vm.eventBus.emit('set_customer', r.message.name);
              vm.eventBus.emit('fetch_customer_details');
              vm.close_dialog();
            } else {
              frappe.utils.play_sound('error');
              vm.eventBus.emit('show_message', {
                title: __('Customer creation failed.'),
                color: 'error',
              });
            }
          },
        });
        this.customerDialog = false;
      }
    },
  },
  created: function () {
    this.eventBus.on('open_update_customer', (data) => {
      this.customerDialog = true;
      if (data) {
        this.customer_name = data.customer_name;
        this.customer_id = data.name;
        this.tax_id = data.tax_id;
        this.mobile_no = data.mobile_no;
        this.email_id = data.email_id;
        this.referral_code = data.referral_code;
        this.birthday = data.birthday;
        this.group = data.customer_group;
        this.territory = data.territory;
        this.loyalty_points = data.loyalty_points;
        this.loyalty_program = data.loyalty_program;
        this.gender = data.gender;
      }
    });
    this.eventBus.on('register_pos_profile', (data) => {
      this.pos_profile = data.pos_profile;
    });
    this.eventBus.on('payments_register_pos_profile', (data) => {
      this.pos_profile = data.pos_profile;
    });
    this.getCustomerGroups();
    this.getCustomerTerritorys();
    this.getGenders();
    // set default values for customer group and territory from user defaults
    this.group = frappe.defaults.get_user_default('Customer Group');
    this.territory = frappe.defaults.get_user_default('Territory');
  },
};
</script>
