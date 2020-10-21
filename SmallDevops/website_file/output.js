var data = [{
 "commit": [
  "6eee3bf49fb019b110c6fd8d0ea419b56a38aeab",
  "<0pb>",
  "fixed issues"
 ],
 "date": "2020-10-2-14-57-53",
 "error_unittest": true,
 "failed_amount": 3,
 "failed_test": {
  "test_get_list_file_deep (test.test_mini.ContainTest)": [
   "===================================================================",
   "ERROR: test_get_list_file_deep (test.test_mini.ContainTest)",
   "----------------------------------------------------------------------",
   "Traceback (most recent call last):",
   "  File \"/mnt/s/programmation/Website/Money_calculator/calc/minifier/test/test_mini.py\", line 144, in test_get_list_file_deep",
   "    list_file = mini.get_list_file([fake_argument])",
   "  File \"/mnt/s/programmation/Website/Money_calculator/calc/minifier/mini.py\", line 93, in get_list_file",
   "    for root, dirs, files in os.walk(path_to_files)",
   "  File \"/mnt/s/programmation/Website/Money_calculator/calc/minifier/mini.py\", line 92, in <listcomp>",
   "    list_files = [os.path.join(root, name)",
   "  File \"/usr/lib/python3.7/os.py\", line 337, in walk",
   "    top = fspath(top)",
   "TypeError: expected str, bytes or os.PathLike object, not list"
  ],
  "test_get_list_file_simple (test.test_mini.ContainTest)": [
   "===================================================================",
   "ERROR: test_get_list_file_simple (test.test_mini.ContainTest)",
   "----------------------------------------------------------------------",
   "Traceback (most recent call last):",
   "  File \"/mnt/s/programmation/Website/Money_calculator/calc/minifier/test/test_mini.py\", line 128, in test_get_list_file_simple",
   "    list_file = mini.get_list_file([self.testing_path])",
   "  File \"/mnt/s/programmation/Website/Money_calculator/calc/minifier/mini.py\", line 93, in get_list_file",
   "    for root, dirs, files in os.walk(path_to_files)",
   "  File \"/mnt/s/programmation/Website/Money_calculator/calc/minifier/mini.py\", line 92, in <listcomp>",
   "    list_files = [os.path.join(root, name)",
   "  File \"/usr/lib/python3.7/os.py\", line 337, in walk",
   "    top = fspath(top)",
   "TypeError: expected str, bytes or os.PathLike object, not list"
  ],
  "test_main_empty (test.test_mini.ContainTest)": [
   "===================================================================",
   "ERROR: test_main_empty (test.test_mini.ContainTest)",
   "----------------------------------------------------------------------",
   "Traceback (most recent call last):",
   "  File \"/mnt/s/programmation/Website/Money_calculator/calc/minifier/test/test_mini.py\", line 371, in test_main_empty",
   "    mini.main([])",
   "  File \"/mnt/s/programmation/Website/Money_calculator/calc/minifier/mini.py\", line 178, in main",
   "    mini_str = get_mini_str(get_correct_file(get_list_file(args[0])))",
   "IndexError: list index out of range",
   "",
   ""
  ]
 },
 "success_amount": 12,
 "success_test": [
  "test_checking_file (test.test_mini.ContainTest) ... ok",
  "test_format_html (test.test_mini.ContainTest) ... ok",
  "test_get_correct_file (test.test_mini.ContainTest) ... ok",
  "test_get_mini_str (test.test_mini.ContainTest) ... ok",
  "test_main_basic (test.test_mini.ContainTest) ... ok",
  "test_main_html_js (test.test_mini.ContainTest) ... ok",
  "test_main_output (test.test_mini.ContainTest) ... ok",
  "test_main_output_js (test.test_mini.ContainTest) ... ok",
  "test_main_random_args (test.test_mini.ContainTest) ... ok",
  "test_manage_args (test.test_mini.ContainTest) ... ok",
  "test_minifier (test.test_mini.ContainTest) ... ok",
  "test_read_content (test.test_mini.ContainTest) ... ok"
 ],
 "timing_function": 0.02,
 "timing_test": 0.076,
 "total_amount": 15
},{
 "commit": [
  "6eee3bf49fb019b110c6fd8d0ea419b56a38aeab",
  "<0pb>",
  "fixed issues"
 ],
 "date": "2020-10-2-14-58-22",
 "error_unittest": true,
 "failed_amount": 3,
 "failed_test": {
  "test_get_list_file_deep (test.test_mini.ContainTest)": [
   "===================================================================",
   "ERROR: test_get_list_file_deep (test.test_mini.ContainTest)",
   "----------------------------------------------------------------------",
   "Traceback (most recent call last):",
   "  File \"/mnt/s/programmation/Website/Money_calculator/calc/minifier/test/test_mini.py\", line 144, in test_get_list_file_deep",
   "    list_file = mini.get_list_file([fake_argument])",
   "  File \"/mnt/s/programmation/Website/Money_calculator/calc/minifier/mini.py\", line 93, in get_list_file",
   "    for root, dirs, files in os.walk(path_to_files)",
   "  File \"/mnt/s/programmation/Website/Money_calculator/calc/minifier/mini.py\", line 92, in <listcomp>",
   "    list_files = [os.path.join(root, name)",
   "  File \"/usr/lib/python3.7/os.py\", line 337, in walk",
   "    top = fspath(top)",
   "TypeError: expected str, bytes or os.PathLike object, not list"
  ],
  "test_get_list_file_simple (test.test_mini.ContainTest)": [
   "===================================================================",
   "ERROR: test_get_list_file_simple (test.test_mini.ContainTest)",
   "----------------------------------------------------------------------",
   "Traceback (most recent call last):",
   "  File \"/mnt/s/programmation/Website/Money_calculator/calc/minifier/test/test_mini.py\", line 128, in test_get_list_file_simple",
   "    list_file = mini.get_list_file([self.testing_path])",
   "  File \"/mnt/s/programmation/Website/Money_calculator/calc/minifier/mini.py\", line 93, in get_list_file",
   "    for root, dirs, files in os.walk(path_to_files)",
   "  File \"/mnt/s/programmation/Website/Money_calculator/calc/minifier/mini.py\", line 92, in <listcomp>",
   "    list_files = [os.path.join(root, name)",
   "  File \"/usr/lib/python3.7/os.py\", line 337, in walk",
   "    top = fspath(top)",
   "TypeError: expected str, bytes or os.PathLike object, not list"
  ],
  "test_main_empty (test.test_mini.ContainTest)": [
   "===================================================================",
   "ERROR: test_main_empty (test.test_mini.ContainTest)",
   "----------------------------------------------------------------------",
   "Traceback (most recent call last):",
   "  File \"/mnt/s/programmation/Website/Money_calculator/calc/minifier/test/test_mini.py\", line 371, in test_main_empty",
   "    mini.main([])",
   "  File \"/mnt/s/programmation/Website/Money_calculator/calc/minifier/mini.py\", line 178, in main",
   "    mini_str = get_mini_str(get_correct_file(get_list_file(args[0])))",
   "IndexError: list index out of range",
   "",
   ""
  ]
 },
 "success_amount": 12,
 "success_test": [
  "test_checking_file (test.test_mini.ContainTest) ... ok",
  "test_format_html (test.test_mini.ContainTest) ... ok",
  "test_get_correct_file (test.test_mini.ContainTest) ... ok",
  "test_get_mini_str (test.test_mini.ContainTest) ... ok",
  "test_main_basic (test.test_mini.ContainTest) ... ok",
  "test_main_html_js (test.test_mini.ContainTest) ... ok",
  "test_main_output (test.test_mini.ContainTest) ... ok",
  "test_main_output_js (test.test_mini.ContainTest) ... ok",
  "test_main_random_args (test.test_mini.ContainTest) ... ok",
  "test_manage_args (test.test_mini.ContainTest) ... ok",
  "test_minifier (test.test_mini.ContainTest) ... ok",
  "test_read_content (test.test_mini.ContainTest) ... ok"
 ],
 "timing_function": 0.02,
 "timing_test": 0.076,
 "total_amount": 15
}]