import artifacts
import yaml


blueprint_1 = """
    tosca_definitions_version: tosca_simple_yaml_1_0
    
    description: Test template of a custom relationship with a configure script
    
    topology_template:
    
      node_templates:
        apache:
          type: tosca.nodes.WebServer
          requirements:
            - host:
                node: web_server
                relationship: my_custom_rel
    
        web_server:
          type: tosca.nodes.Compute
    
      relationship_templates:
        my_custom_rel:
          type: HostedOn
          interfaces:
            Standard:
              start:
                inputs:
                  operation: "start"
                  duration: { get_property: [ SELF, duration ] }
                  variation: { get_property: [ SELF, variation ] }
                  weight: 20
                  log_length: { get_property: [ SELF, log_length ] }
                implementation: scripts/operation.sh
              stop:
                inputs:
                  operation: "stop"
                  duration: { get_property: [ SELF, duration ] }
                  variation: { get_property: [ SELF, variation ] }
                  weight: 20
                  log_length: { get_property: [ SELF, log_length ] }
                implementation: scripts/operation.sh
"""


def test_get_node_templates():
    nodes = artifacts.get_node_templates(yaml.safe_load(blueprint_1))
    assert len(nodes) == 2


def test_get_relationship_templates():
    relationships = artifacts.get_relationship_templates(yaml.safe_load(blueprint_1))
    assert len(relationships) == 1


def test_get_interfaces():
    interfaces = artifacts.get_interfaces(yaml.safe_load(blueprint_1))
    assert len(interfaces) == 2


def test_get_implementations():
    implementations = artifacts.get_implementations(yaml.safe_load(blueprint_1))
    assert implementations == {'scripts/operation.sh'}
