/*
 * Copyright (c) 2024 Airbyte, Inc., all rights reserved.
 */

package io.airbyte.cdk.load.data

import io.airbyte.cdk.load.message.DestinationRecord
import io.airbyte.protocol.models.v0.AirbyteRecordMessageMetaChange.Change
import io.airbyte.protocol.models.v0.AirbyteRecordMessageMetaChange.Reason

open class AirbyteValueIdentityMapper(
    private val meta: DestinationRecord.Meta,
) : AirbyteValueMapper {
    override fun collectFailure(path: List<String>) {
        meta.changes.add(
            DestinationRecord.Change(
                path.joinToString("."),
                Change.NULLED,
                Reason.DESTINATION_SERIALIZATION_ERROR
            )
        )
    }

    override fun mapObject(
        value: ObjectValue,
        schema: ObjectType,
        path: List<String>
    ): AirbyteValue {
        val values = LinkedHashMap<String, AirbyteValue>()
        schema.properties.forEach { (name, field) ->
            values[name] = map(value.values[name] ?: NullValue, field.type, path + name)
        }
        return ObjectValue(values)
    }

    override fun mapObjectWithoutSchema(
        value: ObjectValue,
        schema: ObjectTypeWithoutSchema,
        path: List<String>
    ): AirbyteValue = value

    override fun mapObjectWithEmptySchema(
        value: ObjectValue,
        schema: ObjectTypeWithEmptySchema,
        path: List<String>
    ): AirbyteValue = value

    override fun mapArray(value: ArrayValue, schema: ArrayType, path: List<String>): AirbyteValue {
        return ArrayValue(
            value.values.mapIndexed { index, element ->
                map(element, schema.items.type, path + "[$index]")
            }
        )
    }

    override fun mapArrayWithoutSchema(
        value: ArrayValue,
        schema: ArrayTypeWithoutSchema,
        path: List<String>
    ): AirbyteValue = value

    override fun mapUnion(
        value: AirbyteValue,
        schema: UnionType,
        path: List<String>
    ): AirbyteValue = value

    override fun mapBoolean(value: BooleanValue, path: List<String>): AirbyteValue = value

    override fun mapNumber(value: NumberValue, path: List<String>): AirbyteValue = value

    override fun mapString(value: StringValue, path: List<String>): AirbyteValue = value

    override fun mapInteger(value: IntegerValue, path: List<String>): AirbyteValue = value

    override fun mapDate(value: DateValue, path: List<String>): AirbyteValue = value

    override fun mapTimeWithTimezone(value: TimeValue, path: List<String>): AirbyteValue = value

    override fun mapTimeWithoutTimezone(value: TimeValue, path: List<String>): AirbyteValue = value

    override fun mapTimestampWithTimezone(value: TimestampValue, path: List<String>): AirbyteValue =
        value

    override fun mapTimestampWithoutTimezone(
        value: TimestampValue,
        path: List<String>
    ): AirbyteValue = value

    override fun mapNull(path: List<String>): AirbyteValue = NullValue

    override fun mapUnknown(value: UnknownValue, path: List<String>): AirbyteValue = value
}
