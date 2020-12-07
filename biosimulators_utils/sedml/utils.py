from .data_model import SedDocument, ModelAttributeChange, Task, Report, Plot2D, Plot3D
import re

__all__ = ['validate_doc', 'validate_reference']


def validate_doc(doc, validate_semantics=True):
    """ Validate a SED document

    Args:
        doc (:obj:`SedDocument`): SED document
        validate_semantics (:obj:`bool`, optional): if :obj:`True`, check that SED-ML is semantically valid

    Raises:
        :obj:`ValueError`: if document is invalid (e.g., required ids missing or ids not unique)
    """
    for child_type in ('models', 'simulations', 'data_generators', 'tasks', 'outputs'):
        children = getattr(doc, child_type)

        missing_ids = next((True for child in children if not getattr(child, 'id', None)), False)
        if missing_ids:
            raise ValueError('{} must have ids'.format(child_type))

        if validate_semantics:
            repeated_ids = len(set(getattr(child, 'id', None) for child in children)) < len(children)
            if repeated_ids:
                raise ValueError('{} must have unique ids'.format(child_type))

    if validate_semantics:
        for model in doc.models:
            for change in model.changes:
                if isinstance(change, ModelAttributeChange):
                    if not change.target:
                        raise ValueError('Model change attributes must define a target')

        for sim in doc.simulations:
            if sim.algorithm:
                if not sim.algorithm.kisao_id or not re.match(r'^KISAO_\d{7}$', sim.algorithm.kisao_id):
                    raise ValueError('Algorithm of simulation {} has an invalid KiSAO id: {}'.format(sim.id, sim.algorithm.kisao_id))
                for change in sim.algorithm.changes:
                    if not change.kisao_id or not re.match(r'^KISAO_\d{7}$', change.kisao_id):
                        raise ValueError('Algorithm of simulation {} has an invalid KiSAO id: {}'.format(sim.id, sim.algorithm.kisao_id))

        for task in doc.tasks:
            if isinstance(task, Task):
                validate_reference(task, 'Task {}'.format(task.id), 'model', 'model')
                validate_reference(task, 'Task {}'.format(task.id), 'simulation', 'simulation')

        for data_gen in doc.data_generators:
            for i_var, var in enumerate(data_gen.variables):
                if (not var.target and not var.symbol) or (var.target and var.symbol):
                    raise ValueError('Variables must define a target or symbol')
                if var.target:
                    validate_reference(var, 'Variable {} of data generator "{}"'.format(i_var + 1, data_gen.id), 'task', 'task')
                    validate_reference(var, 'Variable {} of data generator "{}"'.format(i_var + 1, data_gen.id), 'model', 'model')

        for output in doc.outputs:
            if isinstance(output, Report):
                for i_dataset, dataset in enumerate(output.datasets):
                    validate_reference(dataset, 'Dataset {} of report "{}"'.format(
                        i_dataset + 1, output.id), 'data_generator', 'data data generator')

            elif isinstance(output, Plot2D):
                for i_curve, curve in enumerate(output.curves):
                    validate_reference(curve, 'Curve {} of 2D plot "{}"'.format(
                        i_curve + 1, output.id), 'x_data_generator', 'x data data generator')
                    validate_reference(curve, 'Curve {} of 2D plot "{}"'.format(
                        i_curve + 1, output.id), 'y_data_generator', 'y data data generator')

            elif isinstance(output, Plot3D):
                for i_surface, surface in enumerate(output.surfaces):
                    validate_reference(surface, 'Surface {} of 3D plot "{}"'.format(
                        i_surface + 1, output.id), 'x_data_generator', 'x data data generator')
                    validate_reference(surface, 'Surface {} of 3D plot "{}"'.format(
                        i_surface + 1, output.id), 'y_data_generator', 'y data data generator')
                    validate_reference(surface, 'Surface {} of 3D plot "{}"'.format(
                        i_surface + 1, output.id), 'z_data_generator', 'z data data generator')


def validate_reference(obj, obj_label, attr_name, attr_label):
    if not getattr(obj, attr_name):
        raise ValueError('{} must have a {}'.format(obj_label, attr_label))
