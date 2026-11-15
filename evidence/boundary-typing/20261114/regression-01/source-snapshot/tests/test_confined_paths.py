"""Resolve-spelling regressions for Windows publication races and containment."""

import ntpath
import unittest
from pathlib import PureWindowsPath
from unittest.mock import patch

from pixl import graph
from pixl.codec import PixlError


class ConfinedPathsTests(unittest.TestCase):
    def resolve_as(self, root, name, resolved_root, resolved_child):
        """Supply observed Windows resolve results on any test operating system."""
        resolutions = {
            str(PureWindowsPath(root)): resolved_root,
            str(PureWindowsPath(resolved_root) / name): resolved_child,
            # confined normalizes the root before resolving the child.
            str(PureWindowsPath(root) / name): resolved_child,
        }

        class ObservedWindowsPath(PureWindowsPath):
            def resolve(self):
                return type(self)(resolutions.get(str(self), ntpath.normpath(str(self))))

        with patch("pixl.graph.Path", ObservedWindowsPath):
            return graph.confined(root, name)

    def test_drive_child_and_root_extended_spellings_name_the_same_inside_file(self):
        root = "C:/consumer"
        name = "work/artifact.png"
        for resolved_root in ("C:/consumer", "\\\\?\\C:\\consumer"):
            for resolved_child in ("C:/consumer/work/artifact.png",
                                   "\\\\?\\C:\\consumer\\work\\artifact.png"):
                with self.subTest(root=resolved_root, child=resolved_child):
                    result = self.resolve_as(root, name, resolved_root, resolved_child)
                    self.assertEqual(result, PureWindowsPath("C:/consumer/work/artifact.png"))
                    self.assertTrue(result.is_relative_to(PureWindowsPath(root)))

    def test_unc_child_and_root_extended_spellings_name_the_same_inside_file(self):
        root = "//server/share/consumer"
        name = "work/artifact.png"
        for resolved_root in (root, "\\\\?\\UNC\\server\\share\\consumer"):
            for resolved_child in ("//server/share/consumer/work/artifact.png",
                                   "\\\\?\\UNC\\server\\share\\consumer\\work\\artifact.png"):
                with self.subTest(root=resolved_root, child=resolved_child):
                    result = self.resolve_as(root, name, resolved_root, resolved_child)
                    self.assertEqual(result, PureWindowsPath("//server/share/consumer/work/artifact.png"))
                    self.assertTrue(result.is_relative_to(PureWindowsPath(root)))

    def test_resolved_symlink_or_other_drive_still_cannot_escape(self):
        for child in ("\\\\?\\C:\\outside\\artifact.png", "\\\\?\\D:\\consumer\\artifact.png",
                      "\\\\?\\UNC\\elsewhere\\share\\artifact.png"):
            with self.subTest(child=child), self.assertRaisesRegex(PixlError, "path_escape"):
                self.resolve_as("C:/consumer", "link/artifact.png", "C:/consumer", child)

    def test_sibling_with_same_prefix_and_root_itself_are_not_children(self):
        for root, resolved_root, child in (
            ("C:/consumer", "C:/consumer", "\\\\?\\C:\\consumer-more\\artifact.png"),
            ("C:/consumer", "\\\\?\\C:\\consumer", "C:/consumer"),
            ("//server/share/consumer", "//server/share/consumer", "\\\\?\\UNC\\server\\share\\consumer-more\\artifact.png"),
            ("//server/share/consumer", "\\\\?\\UNC\\server\\share\\consumer", "//server/share/consumer"),
        ):
            with self.subTest(root=root, child=child), self.assertRaisesRegex(PixlError, "path_escape"):
                self.resolve_as(root, "link", resolved_root, child)

    def test_normalizing_resolved_paths_does_not_allow_absolute_or_parent_input(self):
        for name in ("C:/consumer/artifact.png", "\\\\?\\C:\\consumer\\artifact.png", "work\\artifact.png",
                     "work:artifact.png", "../outside.png", ""):
            with self.subTest(name=name), self.assertRaisesRegex(PixlError, "path_escape"):
                self.resolve_as("C:/consumer", name, "C:/consumer", "C:/outside.png")

    def test_other_device_namespaces_are_not_reinterpreted_as_normal_paths(self):
        for child in ("\\\\?\\GLOBALROOT\\Device\\HarddiskVolume1\\consumer\\artifact.png",
                      "\\\\.\\C:\\consumer\\artifact.png"):
            with self.subTest(child=child), self.assertRaisesRegex(PixlError, "path_escape"):
                self.resolve_as("C:/consumer", "work/artifact.png", "C:/consumer", child)


if __name__ == "__main__":
    unittest.main()
