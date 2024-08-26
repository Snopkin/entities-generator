SQL to Kotlin Entity Converter
Overview

This Python program converts SQL CREATE TABLE statements into Kotlin data classes. The generated Kotlin code includes the entity class with fields, constants for column names, and methods to map database rows to the entity and vice versa.
Features

    Converts SQL table schema to a Kotlin data class.
    Automatically generates constants for table and column names.
    Includes methods for mapping database rows to entities and creating tuples from entities.

Requirements

    Python 3.x
    Tkinter (comes pre-installed with Python on most platforms)

Installation

    Clone this repository or download the script.
    Ensure that you have Python 3.x installed on your machine.
    No additional libraries are required apart from the standard tkinter library, which is included with Python.

Usage

    Run the Program:
        Open your terminal or command prompt.
        Navigate to the directory where the script is located.
        Run the script using the command:

    bash

    python sql_to_kotlin_converter.py

    Input the SQL:
        A GUI window will open with a text area.
        Paste your SQL CREATE TABLE statement into the text area.

    Convert to Kotlin:
        Click the "Convert to Kotlin" button.
        A file dialog will appear, allowing you to choose where to save the generated Kotlin file.
        The Kotlin file will be saved with a .kt extension.

Input Requirements

The SQL input must follow these guidelines:

    Table Creation: The SQL statement must start with CREATE TABLE followed by the table name.
    Column Definitions: Each column must be defined with a name and data type. The program will recognize common SQL data types and convert them to appropriate Kotlin types.

Example of a Valid Input

sql

    CREATE TABLE payment_terminal (
        id UUID,
        created_on TIMESTAMPTZ,
        created_by BIGINT,
        modified_on TIMESTAMPTZ,
        modified_by BIGINT,
        serial_number TEXT,
        payment_terminal_type TEXT,
        is_multi_connectors BOOLEAN,
        current_language TEXT,
        default_language TEXT,
        current_screen TEXT,
        last_screen_updated TIMESTAMPTZ,
        pre_auth_amount DECIMAL(22, 10),
        currency TEXT,
        last_status TEXT,
        last_status_updated TIMESTAMPTZ
    );

Generated Output

Given the above SQL input, the program will generate a Kotlin data class similar to this:

kotlin
    
    package com.example.model.entity
    
    import java.math.BigDecimal
    import java.time.OffsetDateTime
    import java.util.UUID
    //
    data class PaymentTerminalEntity(
      val id: UUID,
      val createdOn: OffsetDateTime,
      val createdBy: Long,
      val modifiedOn: OffsetDateTime,
      val modifiedBy: Long,
      val serialNumber: String,
      val paymentTerminalType: String,
      val isMultiConnectors: Boolean,
      val currentLanguage: String,
      val defaultLanguage: String,
      val currentScreen: String,
      val lastScreenUpdated: OffsetDateTime,
      val preAuthAmount: BigDecimal,
      val currency: String,
      val lastStatus: String,
      val lastStatusUpdated: OffsetDateTime
    ) {
      companion object {
        const val TABLE_NAME = "payment_terminal"
    
        // column names
        const val ID = "id"
        const val CREATED_ON = "created_on"
        const val CREATED_BY = "created_by"
        const val MODIFIED_ON = "modified_on"
        const val MODIFIED_BY = "modified_by"
        const val SERIAL_NUMBER = "serial_number"
        const val PAYMENT_TERMINAL_TYPE = "payment_terminal_type"
        const val IS_MULTI_CONNECTORS = "is_multi_connectors"
        const val CURRENT_LANGUAGE = "current_language"
        const val DEFAULT_LANGUAGE = "default_language"
        const val CURRENT_SCREEN = "current_screen"
        const val LAST_SCREEN_UPDATED = "last_screen_updated"
        const val PRE_AUTH_AMOUNT = "pre_auth_amount"
        const val CURRENCY = "currency"
        const val LAST_STATUS = "last_status"
        const val LAST_STATUS_UPDATED = "last_status_updated"
    
        fun Row.toPaymentTerminalEntity(): PaymentTerminalEntity {
          return PaymentTerminalEntity(
            id = this.getUUID(ID),
            createdOn = this.getOffsetDateTime(CREATED_ON),
            createdBy = this.getLong(CREATED_BY),
            modifiedOn = this.getOffsetDateTime(MODIFIED_ON),
            modifiedBy = this.getLong(MODIFIED_BY),
            serialNumber = this.getString(SERIAL_NUMBER),
            paymentTerminalType = this.getString(PAYMENT_TERMINAL_TYPE),
            isMultiConnectors = this.getBoolean(IS_MULTI_CONNECTORS),
            currentLanguage = this.getString(CURRENT_LANGUAGE),
            defaultLanguage = this.getString(DEFAULT_LANGUAGE),
            currentScreen = this.getString(CURRENT_SCREEN),
            lastScreenUpdated = this.getOffsetDateTime(LAST_SCREEN_UPDATED),
            preAuthAmount = this.getBigDecimal(PRE_AUTH_AMOUNT),
            currency = this.getString(CURRENCY),
            lastStatus = this.getString(LAST_STATUS),
            lastStatusUpdated = this.getOffsetDateTime(LAST_STATUS_UPDATED)
          )
        }
    
        fun RowSet<Row>.toPaymentTerminalEntities(): List<PaymentTerminalEntity> {
          return this.map { it.toPaymentTerminalEntity() }
        }
      }
      fun toTuple(): Tuple {
        return Tuple.tuple()
          .addUUID(id)
          .addOffsetDateTime(createdOn)
          .addLong(createdBy)
          .addOffsetDateTime(modifiedOn)
          .addLong(modifiedBy)
          .addString(serialNumber)
          .addString(paymentTerminalType)
          .addBoolean(isMultiConnectors)
          .addString(currentLanguage)
          .addString(defaultLanguage)
          .addString(currentScreen)
          .addOffsetDateTime(lastScreenUpdated)
          .addBigDecimal(preAuthAmount)
          .addString(currency)
          .addString(lastStatus)
          .addOffsetDateTime(lastStatusUpdated)
      }
    }

