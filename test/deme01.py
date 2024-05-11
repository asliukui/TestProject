source_field_en= "bd.OPERATEORGID"
# field_no_dot = source_field_en.replace(source_field_en[source_field_en.find('(')+1:source_field_en.find('.')+1],'')
field_no_dot=source_field_en[source_field_en.find('.')+1:]


print(field_no_dot)

print(str(' ').isNone())


