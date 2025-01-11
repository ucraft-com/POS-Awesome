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

    // Log the received event value
    console.log("Received Event Value:", $event);

    try {
        // Parse the event value
        value = parseFloat($event);

        // Log after parsing
        console.log("Parsed Value:", value);

        if (isNaN(value)) {
            value = 0; // Default to 0 if not a valid number
            console.log("Value is NaN, setting to 0");
        } else if (no_negative && value < 0) {
            value = value * -1; // Convert to positive if no_negative is true
            console.log("Converted Negative Value to Positive:", value);
        }

        // Format the value
        value = this.formatFloat($event, precision);

        // Log the formatted value
        console.log("Formatted Value:", value);
    } catch (e) {
        console.error("Error in setFormatedFloat:", e);
        value = 0; // Default to 0 in case of an error
    }

    // Update the field in the element or the component
    if (typeof el === "object") {
        console.log("Updating object field:", field_name, "with value:", value);
        el[field_name] = value;
    } else {
        console.log("Updating component field:", field_name, "with value:", value);
        this[field_name] = value;
    }

    // Log the final return value
    console.log("Returning Value:", value);
    return value;
},
    mounted() {
        this.float_precision =
            frappe.defaults.get_default('float_precision') || 2;
        this.currency_precision =
            frappe.defaults.get_default('currency_precision') || 2;
    }
}
}