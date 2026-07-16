# -*- coding: utf-8 -*-
from lxml import etree

from odoo import api, fields, models, tools


class SmRenamerRule(models.Model):
    _name = "sm.renamer.rule"
    _description = "Renamer Rule"
    _order = "model_name, current_name"

    active = fields.Boolean(default=True)
    current_name = fields.Char(
        required=True,
        help="Exact label text to replace, e.g. 'Customer'.",
    )
    new_name = fields.Char(required=True, help="Replacement label, e.g. 'Client'.")
    model_id = fields.Many2one(
        "ir.model",
        string="Model",
        ondelete="cascade",
        help="Apply the rename only on this model. Leave empty to apply on all models.",
    )
    model_name = fields.Char(string="Model Name", related="model_id.model", store=True)
    lang = fields.Selection(
        selection=lambda self: self.env["res.lang"].get_installed(),
        string="Language",
        help="Apply the rename only in this language. Leave empty for all languages.",
    )

    @api.model
    @tools.ormcache("model_name", "lang")
    def _get_rename_map(self, model_name, lang):
        rules = self.sudo().search_read(
            [
                "|", ("model_name", "=", model_name), ("model_id", "=", False),
                "|", ("lang", "=", lang), ("lang", "=", False),
            ],
            ["current_name", "new_name", "model_name", "lang"],
        )
        # least specific first, so model/language specific rules win
        rules.sort(key=lambda r: (bool(r["model_name"]), bool(r["lang"])))
        return {r["current_name"]: r["new_name"] for r in rules}

    def _clear_renamer_cache(self):
        self.env.registry.clear_caches()

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._clear_renamer_cache()
        return records

    def write(self, vals):
        result = super().write(vals)
        self._clear_renamer_cache()
        return result

    def unlink(self):
        result = super().unlink()
        self._clear_renamer_cache()
        return result


class Base(models.AbstractModel):
    _inherit = "base"

    def _sm_rename_map(self):
        if self._name == "sm.renamer.rule" or "sm.renamer.rule" not in self.env:
            return {}
        return self.env["sm.renamer.rule"]._get_rename_map(
            self._name, self.env.lang or "en_US"
        )

    def _sm_apply_view_rename(self, result):
        mapping = self._sm_rename_map()
        if mapping and result.get("arch"):
            arch = etree.fromstring(result["arch"])
            changed = False
            # covers explicit strings on buttons, pages, fields, labels, ...
            for node in arch.iter():
                current = node.get("string")
                if current and current in mapping:
                    node.set("string", mapping[current])
                    changed = True
            if changed:
                result["arch"] = etree.tostring(arch, encoding="unicode")
        return result

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        result = super().fields_get(allfields=allfields, attributes=attributes)
        mapping = self._sm_rename_map()
        if mapping:
            for description in result.values():
                new_name = mapping.get(description.get("string"))
                if new_name:
                    description["string"] = new_name
        return result

    def fields_view_get(self, view_id=None, view_type="form", toolbar=False, submenu=False):
        result = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )
        return self._sm_apply_view_rename(result)
