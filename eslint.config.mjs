import globals from "globals";
import pluginJs from "@eslint/js";
import pluginVue from "eslint-plugin-vue";
import pluginVuetify from 'eslint-plugin-vuetify'


/** @type {import('eslint').Linter.Config[]} */
export default [
  { files: ["**/*.{js,mjs,cjs,vue}"] },
  { languageOptions: { globals: globals.browser } },
  // pluginJs.configs.recommended,
  ...pluginVue.configs['flat/base'],
  ...pluginVue.configs["flat/essential"],
  ...pluginVuetify.configs['flat/base'],
];