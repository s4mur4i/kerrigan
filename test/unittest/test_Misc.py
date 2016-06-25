import unittest
from misc import Misc
from misc.Logger import logger


class TestMiscMethods(unittest.TestCase):
    def test_str2bool_true(self):
        self.assertTrue(Misc.str2bool("true"))
        self.assertTrue(Misc.str2bool("True"))
        self.assertTrue(Misc.str2bool("t"))
        self.assertTrue(Misc.str2bool("1"))
        self.assertTrue(Misc.str2bool("yes"))

    def test_str2bool_false(self):
        self.assertFalse(Misc.str2bool("false"))
        self.assertFalse(Misc.str2bool("False"))
        self.assertFalse(Misc.str2bool("f"))
        self.assertFalse(Misc.str2bool("0"))
        self.assertFalse(Misc.str2bool("no"))
        self.assertFalse(Misc.str2bool("ILIKECARS"))

    def test_dict_flatten_correct_path(self):
        should_be = {'a_b': 1, 'a_a': 2, 'b': {'a': 3}}
        start = {'a': {'b': 1, 'a': 2}, 'b': {'a': 3}}
        result = Misc.merge_flatten_dict(dictionary=start, key='a')
        self.assertDictEqual(should_be, result)

    def test_dict_flatten_incorrect_path(self):
        should_be = {'a': {'b': 1, 'a': 2}, 'b': {'a': 3}}
        start = {'a': {'b': 1, 'a': 2}, 'b': {'a': 3}}
        result = Misc.merge_flatten_dict(dictionary=start, key='c')
        self.assertDictEqual(should_be, result)

    def test_dict_flatten_correct_path_no_action(self):
        should_be = {'a': {'b': 1, 'a': 2}, 'b': 3}
        start = {'a': {'b': 1, 'a': 2}, 'b': 3}
        result = Misc.merge_flatten_dict(dictionary=start, key='b')
        self.assertDictEqual(should_be, result)

    def test_remove_last_n_chars_default(self):
        string = "12345"
        should_be = "1234"
        result = Misc.remove_last_n_char(string=string)
        self.assertEqual(result, should_be)

    def test_remove_last_n_chars_more_chars(self):
        string = "12345"
        should_be = "123"
        result = Misc.remove_last_n_char(string=string, char_num=2)
        self.assertEqual(result, should_be)

    def test_remove_last_n_chars_non_int(self):
        string = "12345"
        should_be = "12345"
        result = Misc.remove_last_n_char(string=string, char_num="a")
        self.assertEqual(result, should_be)

    def test_join_string_to_list_default(self):
        list = ['a', 'b']
        should_be = "a,b"
        result = Misc.join_list_to_string(list=list)
        self.assertEqual(should_be, result)

    def test_join_string_to_list_special_char(self):
        list = ['a', 'b']
        should_be = "a_b"
        result = Misc.join_list_to_string(list=list, join_with="_")
        self.assertEqual(should_be, result)

    def test_join_string_to_list_invalid_list(self):
        list = "abs"
        should_be = "a_b_s"
        result = Misc.join_list_to_string(list=list, join_with="_")
        self.assertEqual(should_be, result)

    def test_string_to_array_default(self):
        string = "test.test2.test3"
        should_be = ['test', 'test2', 'test3']
        result = Misc.string_to_array(string=string)
        self.assertEqual(should_be, result)

    def test_string_to_array_special_char(self):
        string = "test_test2_test3"
        should_be = ['test', 'test2', 'test3']
        result = Misc.string_to_array(string=string, split_char="_")
        self.assertEqual(should_be, result)

    def test_string_to_array_nothing_to_split(self):
        string = "test"
        should_be = ['test']
        result = Misc.string_to_array(string=string)
        self.assertEqual(should_be, result)

    def test_list_to_multiline_default(self):
        list = ["test", "test2"]
        should_be = "test\ntest2"
        result = Misc.list_to_multiline_string(list=list)
        self.assertEqual(should_be, result)

    def test_list_to_multiline_non_list(self):
        list = "test"
        should_be = "t\ne\ns\nt"
        result = Misc.list_to_multiline_string(list=list)
        self.assertEqual(should_be, result)

    def test_get_value_from_array_hash(self):
        array_hash = [{'Key': 'test', 'Value': 'test_value'}, {'Key': 'test2', 'Value': 'test2_value'}]
        result = Misc.get_value_from_array_hash(dictlist=array_hash, key="test2")
        self.assertEqual("test2_value", result)

    def test_get_value_from_array_hash_invalid_key(self):
        array_hash = [{'Key': 'test', 'Value': 'test_value'}, {'Key': 'test2', 'Value': 'test2_value'}]
        result = Misc.get_value_from_array_hash(dictlist=array_hash, key="test3")
        self.assertEqual(None, result)

    def test_get_value_from_array_hash_empty_array(self):
        array_hash = []
        result = Misc.get_value_from_array_hash(dictlist=array_hash, key="test3")
        self.assertEqual(None, result)

    def test_merge_dicts(self):
        dict_a = {'a': 1, 'b': 2}
        dict_b = {'c': 3, 'd': 4}
        should_be = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        result = Misc.merge_dicts(dict1=dict_a, dict2=dict_b)
        self.assertDictEqual(should_be, result)

    def test_merge_dicts_overlapping_key_same_value(self):
        dict_a = {'a': 1, 'b': 2}
        dict_b = {'b': 2, 'd': 4}
        should_be = {'a': 1, 'b': 2, 'd': 4}
        result = Misc.merge_dicts(dict1=dict_a, dict2=dict_b)
        self.assertDictEqual(should_be, result)

    def test_merge_dicts_overlapping_key_different_value(self):
        dict_a = {'a': 1, 'b': 2}
        dict_b = {'b': 3, 'd': 4}
        with self.assertRaises(Exception) as cm:
            Misc.merge_dicts(dict1=dict_a, dict2=dict_b)
        self.assertTrue('Conflict at b' in cm.exception)

    def test_parse_service_columns_empty(self):
        columns = ""
        keys = Misc.ec2_columns.keys()
        self.assertListEqual(keys, Misc.parse_service_columns(service="ec2",columns=columns))

    def test_parse_service_columns_2_column(self):
        columns = "id,vpc_id,notexist"
        keys = ["id", "vpc_id"]
        self.assertListEqual(keys, Misc.parse_service_columns(service="ec2",columns=columns))

    def test_parse_service_columns_all_column(self):
        keys = Misc.ec2_columns.keys()
        columns = ",".join(keys)
        self.assertListEqual(keys, Misc.parse_service_columns(service="ec2",columns=columns))

    def test_parse_service_columns_with_services_cloudformation(self):
        columns = ""
        keys = Misc.get_supported_columns(service="cloudformation").keys()
        self.assertListEqual(keys, Misc.parse_service_columns(service="cloudformation",columns=columns))

    def test_parse_service_columns_with_services_elb(self):
        columns = ""
        keys = Misc.get_supported_columns(service="elb").keys()
        self.assertListEqual(keys, Misc.parse_service_columns(service="elb",columns=columns))

    def test_format_boto3_filter(self):
        filters = "tag-value:test"
        should_be = [{'Name': 'tag-value', 'Values': ['test']}]
        self.assertEqual(should_be, Misc.format_boto3_filter(filters=filters))

    def test_format_boto3_filter_invalid_filter(self):
        filters = "tag:value:test"
        with self.assertRaises(ValueError) as cm:
            Misc.format_boto3_filter(filters=filters)
        self.assertTrue('too many values to unpack' in cm.exception)

    def test_format_boto3_filter_multiple_values(self):
        filters = "tag-value:test,tag-test:test2"
        should_be = [{'Name': 'tag-value', 'Values': ['test']}, {'Name': 'tag-test', 'Values': ['test2']}]
        self.assertEqual(should_be, Misc.format_boto3_filter(filters=filters))

    def test_parse_arn_base_resource(self):
        test_arn = "arn:partition:service:region:account-id:resource"
        should_be = {'arn': 'arn', 'partition': 'partition', 'service': 'service', 'region': 'region',
                     'account-id': 'account-id', 'resource': 'resource'}
        result = Misc.parse_arn(arn=test_arn)
        self.assertDictEqual(should_be, result)

    def test_parse_arn_base_resource_sub_resouce(self):
        test_arn = "arn:partition:service:region:account-id:resource/resource"
        should_be = {'arn': 'arn', 'partition': 'partition', 'service': 'service', 'region': 'region',
                     'account-id': 'account-id', 'resource': 'resource/resource'}
        result = Misc.parse_arn(arn=test_arn)
        self.assertDictEqual(should_be, result)

    def test_parse_arn_base_resource_extra_column(self):
        test_arn = "arn:partition:service:region:account-id:resource:resource_sub"
        should_be = {'arn': 'arn', 'partition': 'partition', 'service': 'service', 'region': 'region',
                     'account-id': 'account-id', 'resource': 'resource', 'resource_sub': 'resource_sub'}
        result = Misc.parse_arn(arn=test_arn)
        self.assertDictEqual(should_be, result)

    def test_parse_arn_base_resource_invalid_arn(self):
        test_arn = "yes"
        should_be = None
        result = Misc.parse_arn(arn=test_arn)
        self.assertEqual(should_be, result)

    def test_random3digit(self):
        random = Misc.random3digit()
        self.assertRegexpMatches(random,"\d{1,3}")

    def test_get_supported_columns_for_ec2(self):
        should_be = Misc.ec2_columns
        result = Misc.get_supported_columns(service="ec2")
        self.assertEqual(should_be,result)

    def test_get_supported_columns_for_cloudformation(self):
        should_be = Misc.cloudformation_columns
        result = Misc.get_supported_columns(service="cloudformation")
        self.assertEqual(should_be,result)

    def test_get_supported_columns_for_empty(self):
        should_be = None
        result = Misc.get_supported_columns(service="NotExistService")
        self.assertEqual(should_be,result)

# To remove warning and error printing
logger.verbosity = 0
