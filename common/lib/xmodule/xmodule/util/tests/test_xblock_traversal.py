"""
Unit tests for XBlock traversal utilities
"""
from xmodule.modulestore.tests.factories import ItemFactory
from contentstore.tests.utils import CourseTestCase
from xmodule.util import xblock_traversal


class TestGetXBlockParent(CourseTestCase):
    """
    Tests for the get_xblock_parent function
    """

    def setUp(self):
        """
        Initial data setup
        """
        super(TestGetXBlockParent, self).setUp()

        # create chapter
        self.chapter1 = ItemFactory.create(
            parent_location=self.course.location,
            category='chapter',
            display_name='untitled chapter 1'
        )

        # create sequential
        self.seq1 = ItemFactory.create(
            parent_location=self.chapter1.location,
            category='sequential',
            display_name='untitled sequential 1'
        )

        # create vertical
        self.vert1 = ItemFactory.create(
            parent_location=self.seq1.location,
            category='vertical',
            display_name='untitled vertical 1'
        )

    def test_get_direct_parent(self):
        """ Test test_get_direct_parent """

        result = xblock_traversal.get_xblock_parent(self.vert1)
        self.assertEqual(result.location, self.seq1.location)

    def test_get_parent_with_category(self):
        """ Test test_get_parent_of_category """

        result = xblock_traversal.get_xblock_parent(self.vert1, 'sequential')
        self.assertEqual(result.location, self.seq1.location)
        result = xblock_traversal.get_xblock_parent(self.vert1, 'chapter')
        self.assertEqual(result.location, self.chapter1.location)

    def test_get_parent_none(self):
        """ Test test_get_parent_none """

        result = xblock_traversal.get_xblock_parent(self.vert1, 'unit')
        self.assertIsNone(result)
