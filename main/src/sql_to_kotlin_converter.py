from tkinter import Text, filedialog
import tkinter as tk
import re


__author__ = "Lidor Nir Shalom"
class SQLToKotlinConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("SQL to Kotlin Entity Converter")
        self.text_input = tk.Text(root, height=20, width=80)
        self.text_input.pack()
        self.convert_button = tk.Button(root, text="Convert to Kotlin :)", command=self.convert_sql_to_kotlin)
        self.convert_button.pack()

    def convert_sql_to_kotlin(self):
        sql_text = self.text_input.get("1.0", tk.END)
        kotlin_code = self.generate_kotlin_entity(sql_text)

        if kotlin_code:
            output_window = tk.Toplevel(self.root)
            output_window.title("Generated Kotlin Code")

            output_text = tk.Text(output_window, height=100, width=120)
            output_text.pack()

            output_text.insert(tk.END, kotlin_code)

            output_text.config(state=tk.DISABLED)

            scrollbar = tk.Scrollbar(output_window, command=output_text.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            output_text.config(yscrollcommand=scrollbar.set)

    def generate_kotlin_entity(self, sql_text):
        table_name_match = re.search(r'create table (\w+)', sql_text, re.IGNORECASE)
        if not table_name_match:
            return None

        table_name = table_name_match.group(1)
        kotlin_class_name = ''.join(word.capitalize() for word in table_name.split('_')) + "Entity"

        kotlin_code = f"package com.example.model.entity\n\nimport java.math.BigDecimal\nimport java.time.OffsetDateTime\nimport java.util.UUID\n\n"
        kotlin_code += f"data class {kotlin_class_name}(\n"

        columns = re.findall(r'(\w+)\s+([\w\(\)]+)', sql_text[sql_text.lower().find('('):])
        kotlin_fields = []
        column_constants = []
        row_getters = []
        tuple_setters = []

        for col_name, col_type in columns:
            kotlin_type = self.get_kotlin_type(col_type)
            kotlin_fields.append(f"  val {self.to_camel_case(col_name)}: {kotlin_type}")
            column_constants.append(f'    const val {col_name.upper()} = "{col_name}"')
            row_getters.append(
                f'        {self.to_camel_case(col_name)} = this.{self.get_row_method(col_type)}({col_name.upper()})')
            tuple_setters.append(f'      .{self.get_tuple_method(col_type)}({self.to_camel_case(col_name)})')

        kotlin_code += ",\n".join(kotlin_fields)
        kotlin_code += "\n) {\n"

        kotlin_code += "  companion object {\n"
        kotlin_code += f'    const val TABLE_NAME = "{table_name}"\n\n'  # Use the actual table name

        kotlin_code += "    // column names\n"
        kotlin_code += "\n".join(column_constants)
        kotlin_code += "\n\n    fun Row.to" + kotlin_class_name + "(): " + kotlin_class_name + " {\n"
        kotlin_code += "      return " + kotlin_class_name + "(\n"
        kotlin_code += ",\n".join(row_getters)
        kotlin_code += "\n      )\n    }\n\n"

        kotlin_code += "    fun RowSet<Row>.to" + kotlin_class_name + "s(): List<" + kotlin_class_name + "> {\n"
        kotlin_code += "      return this.map { it.to" + kotlin_class_name + "() }\n"
        kotlin_code += "    }\n  }\n\n"

        kotlin_code += "  fun toTuple(): Tuple {\n"
        kotlin_code += "    return Tuple.tuple()\n"
        kotlin_code += "\n".join(tuple_setters)
        kotlin_code += "\n  }\n}\n"

        return kotlin_code

    def get_kotlin_type(self, sql_type):
        type_map = {
            'uuid': 'UUID',
            'text': 'String',
            'varchar': 'String',
            'char': 'String',
            'boolean': 'Boolean',
            'timestamptz': 'OffsetDateTime',
            'timestamp': 'OffsetDateTime',
            'decimal': 'BigDecimal',
            'bigint': 'Long',
            'serial': 'Int',
            'bigserial': 'Long',
            'numeric': 'BigDecimal',
            'int': 'Int'
        }
        sql_type_lower = sql_type.lower()
        for key in type_map:
            if key == sql_type_lower:
                return type_map[key]
        return 'String'  # default to String if type not found

    def to_camel_case(self, snake_str):
        components = snake_str.split('_')
        return components[0] + ''.join(x.capitalize() for x in components[1:])

    def get_row_method(self, sql_type):
        method_map = {
            'uuid': 'getUUID',
            'text': 'getString',
            'varchar': 'getString',
            'char': 'getString',
            'boolean': 'getBoolean',
            'timestamptz': 'getOffsetDateTime',
            'timestamp': 'getOffsetDateTime',
            'decimal': 'getBigDecimal',
            'int': 'getInteger',
            'bigint': 'getLong',
            'serial': 'getInteger',
            'bigserial': 'getLong',
            'numeric': 'getBigDecimal'
        }
        for key in method_map:
            if key in sql_type.lower():
                return method_map[key]
        return 'getString'  # Default to getString if method not found

    def get_tuple_method(self, sql_type):
        method_map = {
            'uuid': 'addUUID',
            'text': 'addString',
            'varchar': 'addString',
            'char': 'addString',
            'boolean': 'addBoolean',
            'timestamptz': 'addOffsetDateTime',
            'timestamp': 'addOffsetDateTime',
            'decimal': 'addBigDecimal',
            'int': 'addInteger',
            'bigint': 'addLong',
            'serial': 'addInteger',
            'bigserial': 'addLong',
            'numeric': 'addBigDecimal'
        }
        for key in method_map:
            if key in sql_type.lower():
                return method_map[key]
        return 'addString'  # default to addString if method not found


if __name__ == "__main__":
    root = tk.Tk()
    app = SQLToKotlinConverter(root)
    root.mainloop()
