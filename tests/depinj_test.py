from unittest import TestCase

import depinj


class ScopedClass:
    pass


class SingletonClass:
    pass


class TestGlobalPyjector(TestCase):
    def setUp(self) -> None:
        depinj.add_scoped(ScopedClass)
        depinj.add_singleton(SingletonClass)

    def test_add_scoped(self):
        scp_1 = depinj.get_scoped(ScopedClass)
        scp_2 = depinj.get_scoped(ScopedClass)
        self.assertFalse(id(scp_1) == id(scp_2))

    def test_add_singleton(self):
        sing_1 = depinj.get_singleton(SingletonClass)
        sing_2 = depinj.get_singleton(SingletonClass)
        self.assertEqual(id(sing_1), id(sing_2))


class TestLocalPyjector(TestCase):
    def setUp(self) -> None:
        self.injector = depinj.Injector()
        self.injector.add_scoped(ScopedClass)
        self.injector.add_singleton(SingletonClass)

    def test_add_scoped(self):
        scp_1 = self.injector.get_scoped(ScopedClass)
        scp_2 = self.injector.get_scoped(ScopedClass)
        self.assertNotEqual(id(scp_1), id(scp_2))

    def test_add_singleton(self):
        sing_1 = self.injector.get_singleton(SingletonClass)
        sing_2 = self.injector.get_singleton(SingletonClass)
        self.assertEqual(id(sing_1), id(sing_2))

    def test_error(self):
        try:
            self.injector.add_scoped(SingletonClass)
        except depinj.InjectorError:
            return
        self.fail()


class AnnotatedClass:
    member_1: int
    member_2: ScopedClass


class TestAnnotatedClass(TestCase):
    def setUp(self) -> None:
        self.injector = depinj.Injector()
        self.injector.add_scoped(AnnotatedClass)
        self.injector.add_scoped(ScopedClass)

    def test_members(self):
        instance = self.injector.get_scoped(AnnotatedClass)
        self.assertIsNone(instance.member_1)
        self.assertIsNotNone(instance.member_2)
        self.assertTrue(isinstance(instance.member_2, ScopedClass))


class SuperClass:
    pass


class ExtendedClass(SuperClass):
    pass


class TestInheritance(TestCase):
    def setUp(self) -> None:
        self.injector = depinj.Injector()
        self.injector.add_scoped((SuperClass, ExtendedClass))

    def test_inheritance(self):
        instance = self.injector.get_scoped(SuperClass)
        self.assertTrue(isinstance(instance, ExtendedClass))


class TestInject(TestCase):
    def setUp(self) -> None:
        depinj.clear()
        depinj.add_scoped(ScopedClass)

        @depinj.inject
        def sample_func(dependency: ScopedClass):
            return type(dependency)

        self.sample_func = sample_func

    def test_inject(self):
        self.assertEqual(self.sample_func(), ScopedClass)
