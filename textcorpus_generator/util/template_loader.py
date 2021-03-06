"""
Template loader

Loads templates in memory and makes them available for generation
"""
import logging

from textcorpus_generator.util.utterance_expander import expand


class TemplateLoader:
    templates = []
    intents = set()

    def __init__(self, file_name: str):
        logger = logging.getLogger(__name__)
        logger.info("Load templates from {file}".format(file=file_name))

        with open(file_name) as fp:
            for line in fp:
                line = line.rstrip()
                if not line.startswith('#') and len(line) > 0:
                    self.templates.extend(expand(line))

        for template in self.templates:
            if ';' in template:
                intent = template.split(';')[1].strip()
                if len(intent) > 0:
                    self.intents.add(intent)
            else:
                logger.warning('Template {template} without intent'.format(template=template))

        logger.info('Load {templates} templates with {intents} distinct intents'.format(templates=len(self.templates), intents=len(self.intents)))

    def get_templates_by_intents(self, expected_intent: str):
        """
        Get all the templates that have the expected_intent intent
        :param expected_intent: expected intent
        :return: List of templates
        """
        templates_by_intents = []
        for template in self.templates:
            if ';' in template:
                intent = template.split(';')[1].strip()
                if len(intent) > 0 and intent == expected_intent:
                    templates_by_intents.append(template)

        return templates_by_intents

