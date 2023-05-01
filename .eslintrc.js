module.exports = {
  env: {
    es6: true,
    node: true,
  },
  parserOptions: {
    ecmaVersion: 2018,
  },
  extends: ["eslint:recommended", "google"],
  rules: {
    "no-restricted-globals": ["error", "name", "length"],
    "prefer-arrow-callback": "error",
    "quotes": ["error", "double", {allowTemplateLiterals: true}],
    "max-len": [
      "error",
      {
        code: 80,
        ignoreComments: true,
        ignoreUrls: true,
        ignoreTrailingComments: true, // eg.: message: "some content", // Our comment... long this line
        ignoreStrings: true,
        ignorePattern: "^\\s*var\\s.+=\\s*require\\s*\\(",
        ignoreTemplateLiterals: true, // eg.: `Long string concat ${expresion|variable}`
      },
    ], // https://eslint.org/docs/latest/rules/max-len
  },
  overrides: [
    {
      files: ["**/*.spec.*"],
      env: {
        mocha: true,
      },
      rules: {},
    },
  ],
  globals: {},
};
