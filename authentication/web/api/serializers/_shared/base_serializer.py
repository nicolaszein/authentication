from marshmallow import Schema


class BaseSerializer(Schema):

    def serialize(self, data, wrapper=None):
        wrapper = wrapper or getattr(self.Meta, 'wrapper', 'data')

        response = {
            wrapper: self.dump(data)
        }

        return response
