<template>
  <v-layout wrap>
    <new-edit-sheet />
    <delete-dialog />
    <div class="headline">Tasks</div>
    <v-spacer />
    <table-filter-dialog />
    <v-btn color="info" class="ml-2" @click="createEditShow()">New</v-btn>
    <v-flex xs12>
      <v-layout column>
        <v-flex>
          <v-card elevation="0">
            <v-card-title>
              <v-text-field
                v-model="q"
                append-icon="search"
                label="Search"
                single-line
                hide-details
                clearable
              />
            </v-card-title>
            <v-data-table
              :headers="headers"
              :items="items"
              :server-items-length="total"
              :page.sync="page"
              :items-per-page.sync="itemsPerPage"
              :sort-by.sync="sortBy"
              :sort-desc.sync="descending"
              v-model="selected"
              :loading="loading"
              loading-text="Loading... Please wait"
              show-select
            >
              <template v-slot:item.description="{ item }">
                <div class="text-truncate" style="max-width: 400px">
                  {{ item.description }}
                </div>
              </template>
              <template v-slot:item.incident_priority.name="{ item }">
                <incident-priority :priority="item.incident.incident_priority.name" />
              </template>
              <template v-slot:item.creator.individual_contact.name="{ item }">
                <participant :participant="item.creator" />
              </template>
              <template v-slot:item.owner.individual_contact.name="{ item }">
                <participant :participant="item.owner" />
              </template>
              <template v-slot:item.incident_type.name="{ item }">
                {{ item.incident.incident_type.name }}
              </template>
              <template v-slot:item.tickets="{ item }">
                <a
                  v-for="ticket in item.tickets"
                  :key="ticket.weblink"
                  :href="ticket.weblink"
                  target="_blank"
                  style="text-decoration: none;"
                >
                  Ticket
                  <v-icon small>open_in_new</v-icon>
                </a>
              </template>
              <template v-slot:item.assignees="{ item }">
                <participant
                  v-for="assignee in item.assignees"
                  :key="assignee.id"
                  :participant="assignee"
                >
                </participant>
              </template>
              <template v-slot:item.resolve_by="{ item }">{{
                item.resolve_by | formatDate
              }}</template>
              <template v-slot:item.created_at="{ item }">{{
                item.created_at | formatDate
              }}</template>
              <template v-slot:item.resolved_at="{ item }"
                >{{ item.resolved_at | formatDate }}
              </template>
              <template v-slot:item.source="{ item }">
                <a :href="item.weblink" target="_blank" style="text-decoration: none;">
                  {{ item.source }}
                  <v-icon small>open_in_new</v-icon>
                </a>
              </template>
              <template v-slot:item.data-table-actions="{ item }">
                <v-menu bottom left>
                  <template v-slot:activator="{ on }">
                    <v-btn icon v-on="on">
                      <v-icon>mdi-dots-vertical</v-icon>
                    </v-btn>
                  </template>
                  <v-list>
                    <v-list-item @click="createEditShow(item)">
                      <v-list-item-title>View / Edit</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </template>
            </v-data-table>
          </v-card>
        </v-flex>
      </v-layout>
    </v-flex>
    <bulk-edit-sheet></bulk-edit-sheet>
  </v-layout>
</template>

<script>
import { mapFields } from "vuex-map-fields"
import { mapActions } from "vuex"
import DeleteDialog from "@/task/DeleteDialog.vue"
import NewEditSheet from "@/task/NewEditSheet.vue"
import TableFilterDialog from "@/task/TableFilterDialog.vue"
import BulkEditSheet from "@/task/BulkEditSheet.vue"
import IncidentPriority from "@/incident/IncidentPriority.vue"
import Participant from "@/incident/Participant.vue"

export default {
  name: "TaskTable",

  components: {
    TableFilterDialog,
    DeleteDialog,
    NewEditSheet,
    BulkEditSheet,
    IncidentPriority,
    Participant
  },
  data() {
    return {
      headers: [
        { text: "Incident Name", value: "incident.name", sortable: true },
        { text: "Incident Priority", value: "incident_priority.name", sortable: true },
        { text: "Incident Type", value: "incident_type.name", sortable: true },
        { text: "Status", value: "status", sortable: true },
        { text: "Creator", value: "creator.individual_contact.name", sortable: true },
        { text: "Owner", value: "owner.individual_contact.name", sortable: true },
        { text: "Assignees", value: "assignees", sortable: false },
        { text: "Description", value: "description", sortable: false },
        { text: "Source", value: "source", sortable: true },
        { text: "Tickets", value: "tickets", sortable: false },
        { text: "Due By", value: "resolve_by", sortable: true },
        { text: "Created At", value: "created_at", sortable: true },
        { text: "Resolved At", value: "resolved_at", sortable: true },
        { text: "", value: "data-table-actions", sortable: false, align: "end" }
      ]
    }
  },

  computed: {
    ...mapFields("task", [
      "table.options.q",
      "table.options.page",
      "table.options.itemsPerPage",
      "table.options.sortBy",
      "table.options.descending",
      "table.options.filters.creator",
      "table.options.filters.assignee",
      "table.options.filters.incident",
      "table.options.filters.incident_type",
      "table.options.filters.incident_priority",
      "table.options.filters.status",
      "table.loading",
      "table.rows.items",
      "table.rows.total",
      "table.rows.selected"
    ])
  },

  mounted() {
    this.getAll({})

    this.$watch(
      vm => [vm.page],
      () => {
        this.getAll()
      }
    )

    this.$watch(
      vm => [
        vm.q,
        vm.itemsPerPage,
        vm.sortBy,
        vm.descending,
        vm.creator,
        vm.assignee,
        vm.incident,
        vm.incident_type,
        vm.incident_priority,
        vm.status
      ],
      () => {
        this.page = 1
        this.getAll()
      }
    )
  },

  methods: {
    ...mapActions("task", ["getAll", "createEditShow", "removeShow"])
  }
}
</script>
