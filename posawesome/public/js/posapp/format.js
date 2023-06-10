export default {
    methods: {
        flt (value, precision, number_format, rounding_method) {
            if (!precision && precision != 0) {
                precision = this.currency_precision || 2;
            }
            if (!rounding_method) {
                rounding_method = "Banker's Rounding (legacy)";
            }
            return flt(value, precision, number_format, rounding_method);
        },
        formtCurrency (value, precision) {
            const fomrat = get_number_format(this.pos_profile?.currency);
            value = format_number(
                value,
                fomrat,
                precision || this.currency_precision || 2
            );
            return value;
        },
        formtFloat (value, precision) {
            const fomrat = get_number_format(this.pos_profile.currency);
            value = format_number(value, fomrat, precision || this.float_precision || 2);
            return value;
        },
        setFormatedCurrency (el, field_name, precision, no_negative = false, $event) {
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
                value = this.formtCurrency($event, precision);
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
        setFormatedFloat (el, field_name, precision, no_negative = false, $event) {
            let value = 0;
            try {
                // make sure it is a number and positive
                value = parseFloat($event);
                if (isNaN(value)) {
                    value = 0;
                } else if (no_negative && value < 0) {
                    value = value * -1;
                }
                value = this.formtCurrency($event, precision);
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
        currencySymbol (currency) {
            return get_currency_symbol(currency);
        },
        isNumber (value) {
            const pattern = /^-?(\d+|\d{1,3}(\.\d{3})*)(,\d+)?$/;
            return pattern.test(value) || "invalid number";

        }
    },
};