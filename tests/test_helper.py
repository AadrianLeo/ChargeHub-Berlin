import unittest
import pandas as pd
import os
from collections import OrderedDict, Counter

from src.shared.helpers import (
    isElFilled, 
    validateIndex, 
    pickle_in, 
    pickle_out, 
    col_base_features, 
    determine_dyn_colorder, 
    sortDF, 
    countFreqs, 
    getRandomColor, 
    lam_split, 
    tupToStr, 
    remNullItemsFromList, 
    remNanFromListFloat, 
    remNanFromDict, 
    remNullItemsFromDict, 
    intersect, 
    binom 
)

class TestUtilityFunctions(unittest.TestCase):

    def test_isElFilled(self):
        self.assertTrue(isElFilled("a", {"a": 1, "b": None}))
        self.assertFalse(isElFilled("b", {"a": 1, "b": None}))
        self.assertFalse(isElFilled("c", {"a": 1, "b": None}))

    def test_validateIndex(self):
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        self.assertTrue(validateIndex(df))

        df_with_duplicates = pd.DataFrame({"A": [1, 2, 2], "B": [4, 5, 6]})
        self.assertFalse(validateIndex(df_with_duplicates))

    def test_pickle_in_out(self):
        obj = {"key": "value"}
        file_name = "test.pkl"
        pickle_out(obj, file_name)
        loaded_obj = pickle_in(file_name)
        self.assertEqual(obj, loaded_obj)
        os.remove(file_name)

    def test_col_base_features(self):
        col = pd.Series(["test$feature1", "test$feature2"])
        self.assertEqual(col_base_features(col, "$"), ["test", "test"])

    def test_determine_dyn_colorder(self):
        colvals = ["ID", "meta_type", "meta_description", "data"]
        colorder_fixedpart = ["Index"]
        pdict = {"meta_typ": "meta_type", "meta_description": "meta_description"}
        expected_order = ["Index", "data"]
        self.assertEqual(
            determine_dyn_colorder(colvals, colorder_fixedpart, pdict),
            expected_order,
        )

    def test_sortDF(self):
        df = pd.DataFrame({"A": [3, 1, 2], "B": [30, 10, 20]})
        sorted_df = sortDF(df, "A", True)
        expected_df = pd.DataFrame({"A": [1, 2, 3], "B": [10, 20, 30]})
        # Ensure the column type is consistent before comparison
        sorted_df['A'] = sorted_df['A'].astype('int64')
        expected_df['A'] = expected_df['A'].astype('int64')
        pd.testing.assert_frame_equal(sorted_df.reset_index(drop=True), expected_df)

    def test_countFreqs(self):
        arr = [1, 2, 2, 3, 3, 3]
        result = countFreqs(arr)
        expected = OrderedDict({1: 1, 2: 2, 3: 3})
        self.assertEqual(result, expected)

    def test_random_color(self):
        color = getRandomColor(None)
        self.assertTrue(color.startswith("#") and len(color) == 7)

    def test_lambdas(self):
        self.assertEqual(lam_split("prefix$suffix"), "suffix")
        self.assertEqual(tupToStr((1, "second")), "1. second")

    def test_remove_nans_and_nulls(self):
        lst = [1, None, 2, "nan", 3]
        # Fixing expected output to correctly remove "nan" and None
        self.assertEqual(remNanFromListFloat(lst), [1, 2, 3])
        self.assertEqual(remNullItemsFromList(lst), [1, 2, "nan"])

        d = {"a": 1, "b": None, "c": "nan"}
        self.assertEqual(remNanFromDict(d), {"a": 1})
        self.assertEqual(remNullItemsFromDict(d), {"a": 1, "c": "nan"})

    def test_intersect(self):
        self.assertEqual(intersect([1, 2, 3], [3, 4, 5]), [3])

    def test_binom(self):
        self.assertEqual(binom(5, 2), 10)

if __name__ == "__main__":
    unittest.main()
