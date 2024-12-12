export default {
    data() {
        return {
            float_precision: 2,
            currency_precision: 2
        };
    },
    methods: {
        flt(value, precision, number_format, rounding_method) {
            if (!precision && precision != 0) {
                precision = this.currency_precision || 2;
            }
            if (!rounding_method) {
                rounding_method = "Banker's Rounding (legacy)";
            }
            return flt(value, precision, number_format, rounding_method);
        },
        formatCurrency(value, precision) {
            const format = get_number_format(this.pos_profile?.currency);
            value = format_number(
                value,
                format,
                precision || this.currency_precision || 2
            );
            return value;
        },
        formatFloat(value, precision) {
            const format = get_number_format(this.pos_profile.currency);
            value = format_number(value, format, precision || this.float_precision || 2);
            return value;
        },
        setFormatedCurrency(el, field_name, precision, no_negative = false, $event) {
            let value = 0;
            try {
                // make sure it is a number and positive
                let _value = parseFloat($event);
                if (!isNaN(_value)) {
                    value = _value;
                }
                if (no_negative && value < 0) {
                    value = value * -1;
                }
                value = this.formatCurrency($event, precision);
            } catch (e) {
                console.error(e);
                value = 0;
            }
            // check if el is an object
            if (typeof el === "object") {
                el[field_name] = value;
            }
            else {
                this[field_name] = value;
            }


            return value;
        },
        setFormatedFloat(el, field_name, precision, no_negative = false, $event) {
            let value = 0;
            try {
                // make sure it is a number and positive
                value = parseFloat($event);
                if (isNaN(value)) {
                    value = 0;
                } else if (no_negative && value < 0) {
                    value = value * -1;
                }
                value = this.formatFloat($event, precision);
            } catch (e) {
                console.error(e);
                value = 0;
            }
            // check if el is an object
            if (typeof el === "object") {
                el[field_name] = value;
            }
            else {
                this[field_name] = value;
            }
            return value;
        },
        currencySymbol(currency) {
            return get_currency_symbol(currency);
        },
        isNumber(value) {
            const pattern = /^-?(\d+|\d{1,3}(\.\d{3})*)(,\d+)?$/;
            return pattern.test(value) || "invalid number";

        }
    },
    mounted() {
        this.float_precision =
            frappe.defaults.get_default('float_precision') || 2;
        this.currency_precision =
            frappe.defaults.get_default('currency_precision') || 2;
    }
};